# bkepub/builder.py
import os
import zipfile
from typing import List, Dict, Optional, Union, Type

# Import from sibling modules
from . import constants
from . import templates
from . import utils
from . import loader # For the load classmethod
from . import conversion # For markdown support
from .metadata import MetadataManager
from .item import (
    ManifestItem, HtmlContentItem, CssStyleItem, ImageItem,
    NavigationItem, NcxItem, FontItem, JavaScriptItem
)
from .exceptions import (
    BkEpubError, ItemNotFoundError, DuplicateItemError, MissingMetadataError,
    EpubWriteError, InvalidArgumentError
)


class EpubBuilder:
    """
    Main class for building and manipulating EPUB 3 files.

    This class provides methods to set metadata, add content items (XHTML, CSS,
    images, etc.), define the reading order (spine), create a table of
    contents, and finally save the result as a valid .epub file. It also
    supports loading existing EPUB files.
    """

    def __init__(self):
        """Initializes a new, empty EPUB structure."""
        self.metadata = MetadataManager()
        self._manifest_items: Dict[str, ManifestItem] = {}
        self._spine_item_refs: List[Dict[str, Union[str, bool]]] = []
        self._toc_entries: List[Dict] = []  # [{'label': str, 'href': str, 'children': [...]}]
        self._landmarks: List[Dict] = []  # [{'label': str, 'href': str, 'type': str}]
        self._cover_image_id: Optional[str] = None
        self._book_id_ref: str = "book-id"  # Default ID ref for unique identifier
        self.opf_file_name: str = constants.OPF_FILE_NAME # Relative to OEBPS dir
        self.oebps_dir: str = constants.OEBPS_DIR_NAME # Name of the main content directory in zip
        self._nav_item_id: str = "nav" # Default ID for the Navigation Document
        self._ncx_id: Optional[str] = "ncx" # Default ID for NCX if included
        self._include_ncx: bool = True # Generate NCX by default for compatibility

        # Initialize with essential metadata
        self.metadata.set_unique_identifier(f"urn:uuid:{utils.generate_unique_id()}", self._book_id_ref)
        self.metadata.set_language(constants.DEFAULT_LANG)
        # Add dcterms:modified automatically (will be updated on save)
        self.metadata._ensure_modified_date()

    # --- Metadata Methods ---

    def set_unique_identifier(self, value: str, identifier_id: str = "book-id"):
        """Sets the unique identifier (e.g., UUID, ISBN) for the EPUB."""
        self.metadata.set_unique_identifier(value, identifier_id)
        self._book_id_ref = identifier_id # Keep track of the ref ID

    def set_title(self, title: str):
        """Sets the main title (dc:title) of the EPUB."""
        self.metadata.set_title(title)

    def set_language(self, lang_code: str):
        """Sets the primary language (dc:language) of the EPUB."""
        self.metadata.set_language(lang_code)

    def add_creator(self, name: str, role: Optional[str] = None, file_as: Optional[str] = None, creator_id: Optional[str] = None):
        """Adds a creator (dc:creator) with optional role and file-as metadata."""
        self.metadata.add_creator(name, role, file_as, creator_id)

    def add_metadata(self, type: str, value: str, attributes: Optional[Dict] = None, **kwargs):
        """
        Adds a generic metadata element (DC, meta, link).

        Use specific methods like set_title, add_creator where available.
        Use this for less common DC elements or custom meta/link tags.

        Args:
            type: 'dc', 'meta', or 'link'.
            value: The text content (for dc/meta) or property value (for meta) or href (for link).
            attributes: Dictionary of attributes for the element.
            **kwargs: Arguments specific to meta (property_attr, refines, scheme) or link (rel, media_type).
                      For DC, 'qualified_tag' should be in `attributes`.
        """
        if type == 'dc':
            q_tag = kwargs.get('qualified_tag')
            if not q_tag: raise InvalidArgumentError("DC type requires 'qualified_tag' (e.g., 'dc:publisher') in kwargs.")
            self.metadata.add_dc(q_tag, value, attributes)
        elif type == 'meta':
            prop = kwargs.get('property_attr')
            if not prop: raise InvalidArgumentError("Meta type requires 'property_attr' in kwargs.")
            refines = kwargs.get('refines')
            meta_id = attributes.get('id') if attributes else None
            scheme = kwargs.get('scheme')
            self.metadata.add_meta(prop, value, refines, meta_id, scheme, **(attributes or {}))
        elif type == 'link':
            rel = kwargs.get('rel')
            if not rel: raise InvalidArgumentError("Link type requires 'rel' attribute in kwargs.")
            href = value # Value is used as href for links
            link_id = attributes.get('id') if attributes else None
            media_type = kwargs.get('media_type')
            self.metadata.add_link(href, rel, link_id, media_type)
        else:
            raise InvalidArgumentError(f"Unknown metadata type: {type}. Use 'dc', 'meta', or 'link'.")

    # --- Item Management ---

    def register_item(self, item: ManifestItem, overwrite: bool = False):
        """
        Registers a ManifestItem instance with the builder.

        Internal method. Use add_item or specific add_ methods for convenience.

        Args:
            item: The ManifestItem instance to register.
            overwrite: If True, allow overwriting an existing item with the same ID.

        Raises:
            DuplicateItemError: If an item with the same ID exists and overwrite is False.
        """
        if not isinstance(item, ManifestItem):
            raise InvalidArgumentError(f"Item must be an instance of ManifestItem, not {type(item)}")
        if item.id in self._manifest_items and not overwrite:
            raise DuplicateItemError(f"Item with ID '{item.id}' already exists.")
        self._manifest_items[item.id] = item

    def add_item(self, item: ManifestItem, overwrite: bool = False):
        """
        Adds a pre-constructed ManifestItem to the EPUB manifest.

        Args:
            item: The ManifestItem (or subclass) instance.
            overwrite: If True, allow overwriting an existing item with the same ID.

        Returns:
            The added ManifestItem instance.
        """
        self.register_item(item, overwrite)
        return item

    def get_item(self, item_id: str) -> ManifestItem:
        """Retrieves a manifest item by its ID."""
        try:
            return self._manifest_items[item_id]
        except KeyError:
            raise ItemNotFoundError(f"Item with ID '{item_id}' not found in manifest.")

    def get_item_by_property(self, property_value: str) -> Optional[ManifestItem]:
        """Finds the first manifest item possessing the given property."""
        for item in self._manifest_items.values():
            if property_value in item.properties:
                return item
        return None

    def remove_item(self, item_id: str):
        """
        Removes an item from the manifest by its ID.

        Note: This currently does *not* automatically remove the item from the
        spine, TOC, or landmarks if it's referenced there. Manual cleanup
        of references might be required.
        """
        if item_id in self._manifest_items:
            del self._manifest_items[item_id]
            # Basic cleanup: remove from spine refs
            self._spine_item_refs = [ref for ref in self._spine_item_refs if ref['idref'] != item_id]
            # TODO: More robust cleanup (TOC, landmarks, cover ref?) needed for a complete solution.
        else:
            raise ItemNotFoundError(f"Item with ID '{item_id}' not found in manifest.")

    def get_manifest_items(self) -> List[ManifestItem]:
        """Returns a list of all registered manifest items."""
        return list(self._manifest_items.values())

    # --- Convenience Content Addition Methods ---

    def add_xhtml(self, file_name: str, content: Union[str, bytes],
                  item_id: Optional[str] = None, nav_title: Optional[str] = None,
                  language: Optional[str] = None) -> HtmlContentItem:
        """Adds an XHTML content document."""
        item_id = item_id or utils.generate_unique_id(prefix="html")
        item = HtmlContentItem(item_id, file_name, utils.ensure_bytes(content), nav_title, language)
        self.register_item(item)
        return item

    def add_css(self, file_name: str, content: Union[str, bytes],
                item_id: Optional[str] = None) -> CssStyleItem:
        """Adds a CSS stylesheet."""
        item_id = item_id or utils.generate_unique_id(prefix="css")
        item = CssStyleItem(item_id, file_name, utils.ensure_bytes(content))
        self.register_item(item)
        return item

    def add_image(self, file_name: str, content: bytes, media_type: Optional[str] = None,
                  item_id: Optional[str] = None) -> ImageItem:
        """Adds an image (JPG, PNG, GIF, SVG)."""
        item_id = item_id or utils.generate_unique_id(prefix="img")
        item = ImageItem(item_id, file_name, content, media_type)
        self.register_item(item)
        return item

    def add_font(self, file_name: str, content: bytes, media_type: Optional[str] = None,
                 item_id: Optional[str] = None) -> FontItem:
        """Adds a font resource (OTF, TTF, WOFF, WOFF2)."""
        item_id = item_id or utils.generate_unique_id(prefix="font")
        item = FontItem(item_id, file_name, content, media_type)
        self.register_item(item)
        return item

    def add_javascript(self, file_name: str, content: Union[str, bytes],
                       item_id: Optional[str] = None) -> JavaScriptItem:
        """Adds a JavaScript file."""
        item_id = item_id or utils.generate_unique_id(prefix="js")
        item = JavaScriptItem(item_id, file_name, utils.ensure_bytes(content))
        self.register_item(item)
        return item

    def add_markdown(self, file_name: str, markdown_content: str,
                     item_id: Optional[str] = None, nav_title: Optional[str] = None,
                     language: Optional[str] = None) -> HtmlContentItem:
        """
        Converts Markdown content to XHTML and adds it as a content document.

        Args:
            file_name: Desired filename (e.g., 'chapter1.xhtml'). Must end with .xhtml or .html.
            markdown_content: The Markdown string to convert.
            item_id: Optional unique ID for the item.
            nav_title: Optional title for use in the TOC.
            language: Optional language code for this document.

        Returns:
            The created HtmlContentItem instance.

        Raises:
            InvalidArgumentError: If filename extension is not suitable.
            BkEpubError: If Markdown conversion fails.
        """
        if not file_name.lower().endswith(('.xhtml', '.html')):
             raise InvalidArgumentError("Filename for Markdown content must end with .xhtml or .html")

        item_id = item_id or utils.generate_unique_id(prefix="md")
        doc_title = nav_title or os.path.splitext(os.path.basename(file_name))[0]
        doc_lang = language or self.metadata.find_dc('dc:language') or constants.DEFAULT_LANG

        # Perform conversion
        try:
            xhtml_content_str = conversion.markdown_to_xhtml(markdown_content, doc_title, doc_lang)
            xhtml_content_bytes = utils.ensure_bytes(xhtml_content_str)
        except Exception as e:
             raise BkEpubError(f"Failed to convert Markdown for '{file_name}': {e}")

        # Add as HtmlContentItem
        item = HtmlContentItem(item_id, file_name, xhtml_content_bytes, nav_title, language)
        self.register_item(item)
        return item

    # --- Spine Management ---

    def add_spine_item(self, item_ref: Union[str, ManifestItem], linear: bool = True):
        """
        Adds an item to the reading order (spine).

        Args:
            item_ref: The ID string or the ManifestItem instance to add.
            linear: If True (default), item is part of the primary reading order.
                    If False, it's auxiliary content (linear="no").

        Raises:
            ItemNotFoundError: If the item_ref ID does not exist in the manifest.
            InvalidArgumentError: If the item is not suitable for the spine (e.g., CSS).
        """
        if isinstance(item_ref, ManifestItem):
            item_id = item_ref.id
            item = item_ref
        else:
            item_id = str(item_ref)
            item = self.get_item(item_id) # Raises ItemNotFoundError if not found

        if not item.is_spine_candidate:
            print(f"Warning: Adding item '{item_id}' ({item.media_type}) to spine, "
                  f"but it might not be suitable (is_spine_candidate=False).")
            # Allow adding non-standard items but warn? Or raise error? Let's warn.
            # raise InvalidArgumentError(f"Item '{item_id}' ({item.media_type}) cannot be added to the spine.")

        # Avoid duplicates in spine list
        if any(ref['idref'] == item_id for ref in self._spine_item_refs):
             print(f"Warning: Item '{item_id}' is already in the spine. Skipping duplicate add.")
             return

        self._spine_item_refs.append({'idref': item_id, 'linear': linear})

    def get_spine_items(self) -> List[ManifestItem]:
        """Returns a list of ManifestItem objects in the spine order."""
        spine_items = []
        for ref in self._spine_item_refs:
            try:
                spine_items.append(self.get_item(ref['idref']))
            except ItemNotFoundError:
                # This should ideally be caught during validation before saving
                print(f"Warning: Spine itemref '{ref['idref']}' not found in manifest. Skipping.")
        return spine_items

    # --- TOC (Navigation Document) Management ---

    def set_toc(self, toc_entries: List[Dict]):
        """
        Sets the Table of Contents structure directly.

        The structure should be a list of dictionaries, where each dictionary
        represents a TOC entry and has keys:
          - 'label': The text to display for the entry.
          - 'href': The relative path (from OEBPS/) to the content file,
                    optionally including a fragment identifier (e.g., 'chapter1.xhtml#section2').
                    This path should match the href of a manifest item.
          - 'children': An optional list of nested entry dictionaries.

        Example:
            builder.set_toc([
                {'label': 'Chapter 1', 'href': 'chap1.xhtml', 'children': [
                    {'label': 'Section 1.1', 'href': 'chap1.xhtml#sec1'},
                ]},
                {'label': 'Chapter 2', 'href': 'chap2.xhtml'},
            ])
        """
        # Basic validation could be added here to check dict keys
        self._toc_entries = toc_entries

    def add_toc_entry(self, label: str, href: str, parent_entry: Optional[Dict] = None):
        """
        Adds a single entry to the Table of Contents.

        Note: For complex nested structures, using set_toc might be easier.

        Args:
            label: The text label for the TOC entry.
            href: The href (relative path from OEBPS/, e.g., 'content/chapter1.xhtml').
                  It should correspond to a manifest item's href.
            parent_entry: If provided, adds this entry as a child of the given
                          parent entry dictionary (must be a dict already in _toc_entries).
        """
        new_entry = {'label': label, 'href': href, 'children': []}
        if parent_entry:
            if 'children' not in parent_entry:
                 parent_entry['children'] = []
            parent_entry['children'].append(new_entry)
        else:
            self._toc_entries.append(new_entry)

    # --- Landmarks Management ---

    def add_landmark(self, label: str, href: str, landmark_type: str):
        """
        Adds a structural landmark (e.g., cover, toc, bodymatter).

        Args:
            label: Descriptive label for the landmark (e.g., "Cover", "Table of Contents").
            href: The relative path (from OEBPS/) to the content file,
                  optionally including a fragment identifier. Should match a manifest item's href.
            landmark_type: The EPUB structural semantics type (e.g., constants.LANDMARK_COVER,
                           constants.LANDMARK_TOC, 'bodymatter').
        """
        if not landmark_type:
            raise InvalidArgumentError("Landmark type cannot be empty.")
        # Basic validation? Ensure href likely points to a real item? Maybe later.
        self._landmarks.append({'label': label, 'href': href, 'type': landmark_type})

    # --- Cover Image ---

    def set_cover_image(self, item_ref: Union[str, ImageItem], add_landmark_entry: bool = True):
        """
        Designates an image item as the EPUB cover image.

        Args:
            item_ref: The ID string or the ImageItem instance of the cover image.
            add_landmark_entry: If True (default), automatically adds a 'cover' landmark
                                pointing to a default XHTML wrapper (if created) or the
                                image itself (less common).

        Raises:
            ItemNotFoundError: If the item_ref ID does not exist.
            InvalidArgumentError: If the item is not an ImageItem.
        """
        if isinstance(item_ref, ImageItem):
            item_id = item_ref.id
            item = item_ref
        else:
            item_id = str(item_ref)
            item = self.get_item(item_id)

        if not isinstance(item, ImageItem):
            raise InvalidArgumentError(f"Item '{item_id}' must be an ImageItem to be set as cover.")

        # Remove cover property from any previously set cover image
        if self._cover_image_id:
            try:
                old_cover = self.get_item(self._cover_image_id)
                old_cover.properties.discard(constants.PROPERTY_COVER_IMAGE)
            except ItemNotFoundError:
                 pass # Old cover was removed perhaps

        # Add property to the new cover image
        item.properties.add(constants.PROPERTY_COVER_IMAGE)
        self._cover_image_id = item_id

        # Optionally add landmark (Points to the image href directly for now,
        # common practice is to point to an XHTML file containing the image)
        if add_landmark_entry:
            # Check if a cover landmark already exists
            if not any(lmk['type'] == constants.LANDMARK_COVER for lmk in self._landmarks):
                self.add_landmark("Cover", item.href, constants.LANDMARK_COVER)
            else:
                 # Update existing cover landmark? Or just leave it? Leave for now.
                 print(f"Info: Cover landmark already exists. Not adding/modifying automatically.")

    # --- NCX Generation Control ---
    def set_include_ncx(self, include: bool):
        """Sets whether to generate a toc.ncx file for EPUB 2 compatibility."""
        self._include_ncx = include

    # --- Generation and Saving ---

    def _validate(self):
        """Performs basic validation before saving."""
        print("Validating EPUB structure...")
        # 1. Validate Metadata
        try:
            self.metadata.validate_required()
            # Ensure the unique ID ref points to a real element
            unique_id_ref = self.metadata.get_unique_identifier_ref()
            if not unique_id_ref:
                 raise MissingMetadataError("Package unique-identifier reference could not be determined.")
            # Try finding the element - MetadataManager doesn't expose direct lookup by ID easily
            found_id_element = False
            for ns, tag, text, attrs in self.metadata.get_metadata_elements():
                 if attrs.get('id') == unique_id_ref:
                      found_id_element = True
                      break
            if not found_id_element:
                 raise MissingMetadataError(f"Unique identifier element with id='{unique_id_ref}' not found in metadata.")

        except MissingMetadataError as e:
            raise MissingMetadataError(f"Metadata validation failed: {e}")

        # 2. Validate Spine
        if not self._spine_item_refs:
            raise BkEpubError("Spine validation failed: Spine cannot be empty.")
        for ref in self._spine_item_refs:
            if ref['idref'] not in self._manifest_items:
                raise ItemNotFoundError(f"Spine validation failed: Spine itemref '{ref['idref']}' not found in manifest.")

        # 3. Validate Navigation Document (must exist)
        try:
             self.get_item(self._nav_item_id)
        except ItemNotFoundError:
             # Nav doc should be generated before validation if not present
             raise BkEpubError(f"Navigation Document (item ID: '{self._nav_item_id}') not found or generated.")

        # 4. Validate Cover Image Reference (if set)
        if self._cover_image_id:
            try:
                cover_item = self.get_item(self._cover_image_id)
                if constants.PROPERTY_COVER_IMAGE not in cover_item.properties:
                     print(f"Warning: Cover image ID '{self._cover_image_id}' is set, but item lacks 'cover-image' property.")
                     # Optionally re-add it: cover_item.properties.add(constants.PROPERTY_COVER_IMAGE)
            except ItemNotFoundError:
                raise ItemNotFoundError(f"Cover image ID '{self._cover_image_id}' is set, but item not found in manifest.")

        # 5. Check TOC/Landmark hrefs? (More complex validation)
        # Could check if hrefs roughly correspond to manifest item hrefs.

        print("Validation passed.")

    def _prepare_for_save(self):
        """Ensures core generated files (NAV, NCX) exist before saving."""
        print("Preparing core EPUB files...")
        # Update modification date
        self.metadata._ensure_modified_date()

        # Ensure Navigation Document exists
        if self._nav_item_id not in self._manifest_items:
            print(f"Generating Navigation Document (nav.xhtml)...")
            nav_item = self._generate_nav_xhtml()
            self.register_item(nav_item, overwrite=True) # Add/overwrite NAV item
        else:
            # Regenerate NAV content if TOC/landmarks might have changed
             print(f"Regenerating content for existing Navigation Document (nav.xhtml)...")
             nav_item = self._generate_nav_xhtml()
             existing_item = self.get_item(self._nav_item_id)
             if isinstance(existing_item, NavigationItem):
                 existing_item.content = nav_item.content # Update content
             else: # Should not happen if ID is correct
                  print(f"Warning: Item with NAV ID '{self._nav_item_id}' exists but is not a NavigationItem. Re-registering.")
                  self.register_item(nav_item, overwrite=True)

        # Ensure NCX exists if requested
        if self._include_ncx:
            ncx_item_id = self._ncx_id or "ncx" # Ensure we have an ID
            if ncx_item_id not in self._manifest_items:
                 print(f"Generating NCX Table of Contents ({constants.TOC_NCX_FILE_NAME})...")
                 ncx_item = self._generate_ncx(ncx_item_id)
                 if ncx_item: self.register_item(ncx_item, overwrite=True)
            else:
                 print(f"Regenerating content for existing NCX ({constants.TOC_NCX_FILE_NAME})...")
                 ncx_item = self._generate_ncx(ncx_item_id)
                 if ncx_item:
                      existing_ncx = self.get_item(ncx_item_id)
                      existing_ncx.content = ncx_item.content # Update content
        elif self._ncx_id and self._ncx_id in self._manifest_items:
             # Remove NCX if it exists but is no longer included
             print(f"Removing NCX item '{self._ncx_id}' as include_ncx is False.")
             del self._manifest_items[self._ncx_id]
             self._ncx_id = None # Clear the reference


    def _generate_nav_xhtml(self) -> NavigationItem:
        """Generates the NavigationItem with its XHTML content."""
        nav_lang = self.metadata.find_dc('dc:language') or constants.DEFAULT_LANG
        nav_title = self.metadata.find_dc('dc:title') or "EPUB"

        # Ensure hrefs in TOC/Landmarks are relative to OEBPS/ (which item.href should be)
        # No extra processing needed here if add_toc_entry/add_landmark store correct hrefs
        nav_content_bytes = templates.generate_nav_xhtml(
            book_title=nav_title,
            toc_entries=self._toc_entries,
            landmarks=self._landmarks,
            language=nav_lang
        )
        nav_item = NavigationItem(item_id=self._nav_item_id, content=nav_content_bytes)
        return nav_item

    def _generate_ncx(self, item_id: str) -> Optional[NcxItem]:
        """Generates the NcxItem with its XML content."""
        uid_val = self.metadata.find_dc('dc:identifier', {'id': self._book_id_ref})
        if not uid_val:
             # Fallback to first identifier if specific one not found
             identifiers = self.metadata.find_all_dc('dc:identifier')
             if identifiers: uid_val = identifiers[0][0]
             else: uid_val = f"urn:uuid:{utils.generate_unique_id()}" # Should not happen if validated

        title = self.metadata.find_dc('dc:title') or "Untitled"

        if not self._toc_entries:
            print("Warning: Cannot generate NCX because TOC entries are empty.")
            return None

        # Ensure hrefs are relative to OEBPS/
        ncx_content_bytes = templates.generate_ncx(
            book_uid=uid_val or '',
            book_title=title,
            toc_entries=self._toc_entries
        )
        ncx_item = NcxItem(item_id=item_id, content=ncx_content_bytes)
        return ncx_item

    def _generate_opf(self) -> bytes:
        """Generates the OPF file content."""
        print("Generating OPF content...")
        spine_toc_ref = self._ncx_id if self._include_ncx and self._ncx_id in self._manifest_items else None

        opf_content_bytes = templates.generate_opf(
            unique_identifier_ref=self._book_id_ref,
            metadata_elements=self.metadata.get_metadata_elements(), # Gets validated/finalized list
            manifest_items=list(self._manifest_items.values()),
            spine_items=self._spine_item_refs,
            spine_toc_ref=spine_toc_ref
        )
        return opf_content_bytes

    def _generate_container_xml(self) -> bytes:
        """Generates the META-INF/container.xml content."""
        print("Generating container.xml...")
        # Path to OPF relative to the root of the zip archive
        opf_path_in_zip = f"{self.oebps_dir}/{self.opf_file_name}".replace("\\", "/")
        container_content_bytes = templates.generate_container_xml(opf_path=opf_path_in_zip)
        return container_content_bytes

    def save(self, file_path: str):
        """
        Builds and saves the EPUB file to the specified path.

        Args:
            file_path: The path where the .epub file will be saved.

        Raises:
            EpubWriteError: If any error occurs during file writing or validation.
            MissingMetadataError: If required metadata is missing.
            ItemNotFoundError: If referenced items (spine, cover) are missing.
            BkEpubError: For other EPUB construction errors.
        """
        print(f"Attempting to save EPUB to: {file_path}")
        try:
            # 1. Prepare core generated files (NAV, NCX) and update metadata
            self._prepare_for_save()

            # 2. Validate the structure before proceeding
            self._validate()

            # 3. Generate core XML file contents
            container_xml = self._generate_container_xml()
            opf_content = self._generate_opf()

            # 4. Create the EPUB ZIP archive
            print("Creating EPUB archive...")
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True) # Ensure target dir exists
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as epub_zip:

                # Write mimetype file FIRST and UNCOMPRESSED
                epub_zip.writestr('mimetype', constants.MEDIA_TYPE_EPUB, compress_type=zipfile.ZIP_STORED)

                # Write container.xml
                container_path = 'META-INF/container.xml'
                epub_zip.writestr(container_path, container_xml)

                # Write OPF file
                opf_path_in_zip = f"{self.oebps_dir}/{self.opf_file_name}".replace("\\", "/")
                epub_zip.writestr(opf_path_in_zip, opf_content)

                # Write all manifest items
                print(f"Writing {len(self._manifest_items)} manifest items...")
                for item in self._manifest_items.values():
                    item_path = item.full_path_in_zip # Path relative to zip root (e.g., OEBPS/...)
                    if not item.content:
                        print(f"Warning: Item '{item.id}' ({item.href}) has no content. Skipping writing.")
                        continue
                    try:
                        # print(f"  Writing item '{item.id}' to '{item_path}' ({len(item.content)} bytes)")
                        epub_zip.writestr(item_path, item.content)
                    except Exception as e:
                        raise EpubWriteError(f"Failed to write item '{item.id}' ({item_path}) to EPUB: {e}")

            print(f"EPUB file saved successfully: {file_path}")

        except (MissingMetadataError, ItemNotFoundError, BkEpubError, InvalidArgumentError) as e:
            # Re-raise specific validation/setup errors
            raise EpubWriteError(f"EPUB validation or setup failed: {e}")
        except Exception as e:
            # Catch other unexpected errors during saving
             raise EpubWriteError(f"An unexpected error occurred while saving EPUB to '{file_path}': {e}")

    # --- Loading ---

    @classmethod
    def load(cls, epub_path: str) -> 'EpubBuilder':
        """
        Loads an existing EPUB file into an EpubBuilder instance.

        Args:
            epub_path: Path to the .epub file.

        Returns:
            An EpubBuilder instance populated with the EPUB's content and metadata.

        Raises:
            FileNotFoundError: If the epub_path does not exist.
            EpubParseError: If the EPUB structure is invalid or parsing fails.
        """
        print(f"Loading EPUB from: {epub_path}")
        # Delegate the actual loading logic to the loader module
        return loader.load_epub(epub_path)