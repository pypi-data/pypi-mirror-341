from PySide2 import QtWidgets, QtCore
from ciohoudini.buttoned_scroll_panel import ButtonedScrollPanel
from ciohoudini import utils, validation, payload, render_rops, cameras

import ciocore.loggeria
import hou
import os

logger = ciocore.loggeria.get_conductor_logger()

class SelectionTab(ButtonedScrollPanel):
    def __init__(self, dialog):
        super(SelectionTab, self).__init__(
            dialog,
            buttons=[("close", "Close"), ("continue", "Continue Submission")]
        )
        self.dialog = dialog
        self.node = self.dialog.node
        self.all_checkboxes = []  # Keep track of all node checkboxes
        self.node_map = {}  # Map checkboxes to their corresponding nodes
        self.camera_rop_dict = {}
        self.rop_checkboxes = []  # Keep track of all rop checkboxes
        self.configure_signals()

        # Add "Select all nodes" and "Deselect all nodes" buttons at the top
        self.add_global_buttons()

    def configure_signals(self):
        """Connect button signals to their respective handlers."""
        self.buttons["close"].clicked.connect(self.dialog.on_close)
        self.buttons["continue"].clicked.connect(self.on_continue)

    def add_global_buttons(self):
        """Add global buttons for selecting and deselecting all nodes."""
        button_layout = QtWidgets.QHBoxLayout()
        select_all_button = QtWidgets.QPushButton("Select all nodes")
        deselect_all_button = QtWidgets.QPushButton("Deselect all nodes")

        # Connect the buttons to their respective slots
        select_all_button.clicked.connect(self.select_all_nodes)
        deselect_all_button.clicked.connect(self.deselect_all_nodes)

        # Add buttons to the layout
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(deselect_all_button)
        self.layout.addLayout(button_layout)

    def list_stage_cameras(self, node):
        """
        Lists the name of each rop connected to the generator node and adds checkboxes for nodes in the rops.
        """
        logger.debug("Selection tab: Listing rop nodes...")

        if not node:
            logger.debug("Selection tab: No node provided.")
            return

        # Clear existing content in the layout to prepare for new content
        self.clear()
        self.all_checkboxes = []  # Reset the list of all node checkboxes
        self.node_map = {}  # Reset the node map
        self.camera_rop_dict = {}
        self.rop_checkboxes = []  # Reset the list of rop checkboxes


        # Add the global buttons again at the top
        self.add_global_buttons()

        render_rops_data = render_rops.get_render_rop_data(node)
        for render_rop in render_rops_data:
            rop_path = render_rop.get("path", None)
            camera_list = cameras.find_stage_cameras(rop_path)

            # Create a horizontal layout for the rop title and checkbox
            rop_row_layout = QtWidgets.QHBoxLayout()

            # Create a checkbox for the rop
            rop_checkbox = QtWidgets.QCheckBox()
            rop_checkbox.setToolTip(f"Toggle all cameras in rop: {rop_path}")
            rop_row_layout.addWidget(rop_checkbox)
            self.rop_checkboxes.append(rop_checkbox)  # Track rop checkbox globally

            # Create a label for the rop name and style it
            rop_name_label = QtWidgets.QLabel(f"Rop: {rop_path}")
            rop_name_label.setStyleSheet("font-weight: bold;")  # Make the text bold
            rop_row_layout.addWidget(rop_name_label)

            # Align rop name to the left
            rop_row_layout.setAlignment(QtCore.Qt.AlignLeft)

            # Add the rop row layout to the main layout
            self.layout.addLayout(rop_row_layout)

            # Create a vertical layout to group checkboxes for nodes within the rop
            node_container_layout = QtWidgets.QVBoxLayout()
            node_container_layout.setContentsMargins(40, 0, 0, 0)  # Indent for better grouping
            self.layout.addLayout(node_container_layout)

            # Add checkboxes for each node in the rop
            node_checkboxes = []
            for camera_path in camera_list:
                self.camera_rop_dict[camera_path] = render_rop  # Map camera path to its render_rop
                # logger.debug(f"Adding checkbox for node: {child_node.name()}")
                checkbox = QtWidgets.QCheckBox(camera_path)
                node_container_layout.addWidget(checkbox)
                node_checkboxes.append(checkbox)
                self.all_checkboxes.append(checkbox)  # Track globally
                self.node_map[checkbox] = camera_path  # Map checkbox to its node

            # Connect the rop checkbox to toggle all child node checkboxes
            rop_checkbox.stateChanged.connect(
                lambda state, checkboxes=node_checkboxes: self.toggle_rop_nodes(state, checkboxes)
            )
        # print(self.node_map.items())
        # Add a stretch to align content to the top
        self.layout.addStretch()

    def toggle_rop_nodes(self, state, checkboxes):
        """
        Toggles the state of all node checkboxes under a rop.

        Args:
            state (int): The state of the rop checkbox (0: unchecked, 2: checked).
            checkboxes (list): List of node checkboxes under the rop.
        """
        is_checked = state == QtCore.Qt.Checked
        for checkbox in checkboxes:
            checkbox.setChecked(is_checked)

    def select_all_nodes(self):
        """Sets all node and rop checkboxes to checked."""
        logger.debug("Selecting all nodes...")
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(True)
        for rop_checkbox in self.rop_checkboxes:
            rop_checkbox.setChecked(True)

    def deselect_all_nodes(self):
        """Sets all node and rop checkboxes to unchecked."""
        logger.debug("Deselecting all nodes...")
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(False)
        for rop_checkbox in self.rop_checkboxes:
            rop_checkbox.setChecked(False)
    def get_payloads(self):
        """
        Generates payloads for all checked nodes.

        Returns:
            list: A list of payloads for all checked nodes.
        """
        logger.debug("Generating payloads for all checked nodes...")
        payload_list = []
        kwargs = {}  # Add any additional arguments needed for payload generation

        for checkbox, camera_path in self.node_map.items():
            if checkbox.isChecked():  # Process only checked nodes
                render_rop = self.camera_rop_dict.get(camera_path) # Use .get for safety
                if not render_rop:
                    # logger.warning(f"Could not find render_rop mapping for camera {camera_path}. Skipping payload.")
                    continue

                rop_path = render_rop.get("path", None)
                if not rop_path:
                    # logger.warning(f"Render ROP data for camera {camera_path} is missing 'path'. Skipping payload.")
                    continue

                #logger.debug(f"Generating payload for camera: {camera_path} and rop: {rop_path}")
                kwargs["override_camera"] = camera_path

                # --- Cross-platform path handling ---
                # Houdini node paths and USD prim paths use forward slashes ('/') universally.
                # os.path.basename works correctly with forward slashes even on Windows.
                rop_name = os.path.basename(rop_path)
                camera_name = os.path.basename(camera_path)

                # Get the hip folder (directory containing the .hip file)
                output_folder = None
                hip_folder = hou.getenv("HIP")
                if hip_folder:
                    hip_folder = os.path.abspath(hip_folder)  # Ensure it's an absolute path
                    # Construct the output folder path using os.path.join for cross-platform compatibility
                    # This ensures the correct separators ('/' or '\') are used.
                    output_folder = os.path.join(hip_folder, "render", rop_name, camera_name)

                if not hip_folder:
                    # Get the 'output_folder' parameter from self.node if HIP is not set
                    ren_folder = self.node.parm("output_folder").eval()
                    output_folder = os.path.join(ren_folder, rop_name, camera_name)

                if output_folder:
                    kwargs["camera_output_folder"] = output_folder
                    # --- Construct image filename pattern as requested ---
                    # Get the hip file basename without the extension
                    hip_basename = os.path.splitext(hou.hipFile.basename())[0]
                    if not hip_basename:
                        hip_basename = "untitled"  # Fallback if scene not saved

                    # Construct the image filename pattern using an f-string
                    # The remaining part, "$F4.exr", will be adding in the render script
                    image_filename_pattern = f"{hip_basename}_{rop_name}_{camera_name}_"
                    # Construct the full output path pattern including the folder
                    # This uses os.path.join to ensure cross-platform compatibility.
                    camera_output_path = os.path.join(output_folder, image_filename_pattern)
                    kwargs["camera_output_path"] = camera_output_path
                    # print(f"Camera output path: {camera_output_path}")
                    # print(kwargs)

                # logger.debug(f"Setting output folder for payload: {output_folder}")
                # print(f"Setting output folder for payload: {output_folder}")
                # --- End cross-platform path handling ---

                kwargs["task_limit"] = -1 # Ensure all tasks are generated for the payload
                try:
                    # Assuming get_payload handles the kwargs correctly
                    node_payload = payload.get_payload(self.node, render_rop, **kwargs)
                    if node_payload:
                        payload_list.append(node_payload)
                except Exception as e:
                    logger.error(f"Error generating payload for node {self.node.name()} with ROP {rop_path} and Camera {camera_path}: {e}", exc_info=True) # Add exc_info for traceback

        return payload_list
    def get_payloads_original(self):
        """
        Generates payloads for all checked nodes.

        Returns:
            list: A list of payloads for all checked nodes.
        """
        logger.debug("Generating payloads for all checked nodes...")
        payload_list = []
        kwargs = {}  # Add any additional arguments needed for payload generation

        for checkbox, camera_path in self.node_map.items():
            if checkbox.isChecked():  # Process only checked nodes
                render_rop = self.camera_rop_dict[camera_path]
                rop_path = render_rop.get("path", None)
                logger.debug(f"Generating payload for camera: {camera_path} and rop: {rop_path}")
                kwargs["override_camera"] = camera_path

                #if rop_path = "/stage/usdrender_rop1": use usdrender_rop1 without the /stage prefix
                rop_name = rop_path.split("/")[-1]
                # if camera_path = "/camera_rig_sphere/Instance1": use the last part of the path, which is Instance1
                camera_name = camera_path.split("/")[-1]
                # Get the hip folder
                hip_folder = hou.getenv("HIP")
                # Get the output folder for the render
                output_folder = f"{hip_folder}/render/{rop_name}/{camera_name}"
                kwargs["output_folder"] = output_folder

                kwargs["task_limit"] = -1
                try:
                    node_payload = payload.get_payload(self.node, render_rop, **kwargs)
                    # logger.debug(f"Payload for node {node.name()}: {node_payload}")
                    if node_payload:
                        payload_list.append(node_payload)
                except Exception as e:
                    logger.error(f"Error generating payload for node {self.node.name()}: {e}")

        return payload_list

    def on_continue(self):
        """Handles the 'Continue Submission' button click."""
        logger.debug("Validation tab: Continue Submission...")

        # Generate payloads for all checked nodes
        self.dialog.payloads = self.get_payloads()
        logger.debug(f"Generated {len(self.dialog.payloads)} payloads.")
        # logger.debug("Payloads: ", payloads)

        if self.node:
            # Show the validation tab in the dialog
            self.dialog.show_validation_tab()
            logger.debug("Validation tab: Running validation...")

            # Run validation and populate the validation tab with results
            errors, warnings, notices = validation.run(self.node)
            logger.debug("Validation tab: Populating validation results...")
            self.dialog.validation_tab.populate(errors, warnings, notices)
