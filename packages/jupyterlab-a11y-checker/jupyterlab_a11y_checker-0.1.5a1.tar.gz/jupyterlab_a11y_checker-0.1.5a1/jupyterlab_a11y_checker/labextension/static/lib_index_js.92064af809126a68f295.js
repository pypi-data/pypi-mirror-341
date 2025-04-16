"use strict";
(self["webpackChunka11y_checker"] = self["webpackChunka11y_checker"] || []).push([["lib_index_js"],{

/***/ "./lib/components/FixWidget.js":
/*!*************************************!*\
  !*** ./lib/components/FixWidget.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ImageAltFixWidget: () => (/* binding */ ImageAltFixWidget),
/* harmony export */   TableCaptionFixWidget: () => (/* binding */ TableCaptionFixWidget),
/* harmony export */   TableHeaderFixWidget: () => (/* binding */ TableHeaderFixWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_ai_utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/ai-utils */ "./lib/utils/ai-utils.js");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);



class FixWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(issue, cell, aiEnabled) {
        super();
        this.issue = issue;
        this.cell = cell;
        this.aiEnabled = aiEnabled;
    }
    // Method to remove the widget from the DOM
    removeIssueWidget() {
        const issueWidget = this.node.closest('.issue-widget');
        if (issueWidget) {
            const category = issueWidget.closest('.category');
            issueWidget.remove();
            if (category && !category.querySelector('.issue-widget')) {
                category.remove();
            }
        }
        this.cell.node.style.transition = 'background-color 0.5s ease';
        this.cell.node.style.backgroundColor = '#28A745';
        setTimeout(() => {
            this.cell.node.style.backgroundColor = '';
        }, 1000);
    }
}
// TextFields
class TextFieldFixWidget extends FixWidget {
    constructor(issue, cell, aiEnabled) {
        super(issue, cell, aiEnabled);
        // Simplified DOM structure
        this.node.innerHTML = `
        <div class="textfield-fix-widget">
          <input type="text" class="jp-a11y-input" placeholder="Input text here...">
          <div class="textfield-buttons">
              <button class="jp-Button2 suggest-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" fill-rule="evenodd"><path d="m12.594 23.258l-.012.002l-.071.035l-.02.004l-.014-.004l-.071-.036q-.016-.004-.024.006l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.016-.018m.264-.113l-.014.002l-.184.093l-.01.01l-.003.011l.018.43l.005.012l.008.008l.201.092q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.003-.011l.018-.43l-.003-.012l-.01-.01z"/><path fill="#fff" d="M19 19a1 1 0 0 1 .117 1.993L19 21h-7a1 1 0 0 1-.117-1.993L12 19zm.631-14.632a2.5 2.5 0 0 1 0 3.536L8.735 18.8a1.5 1.5 0 0 1-.44.305l-3.804 1.729c-.842.383-1.708-.484-1.325-1.326l1.73-3.804a1.5 1.5 0 0 1 .304-.44L16.096 4.368a2.5 2.5 0 0 1 3.535 0m-2.12 1.414L6.677 16.614l-.589 1.297l1.296-.59L18.217 6.49a.5.5 0 1 0-.707-.707M6 1a1 1 0 0 1 .946.677l.13.378a3 3 0 0 0 1.869 1.87l.378.129a1 1 0 0 1 0 1.892l-.378.13a3 3 0 0 0-1.87 1.869l-.129.378a1 1 0 0 1-1.892 0l-.13-.378a3 3 0 0 0-1.869-1.87l-.378-.129a1 1 0 0 1 0-1.892l.378-.13a3 3 0 0 0 1.87-1.869l.129-.378A1 1 0 0 1 6 1m0 3.196A5 5 0 0 1 5.196 5q.448.355.804.804q.355-.448.804-.804A5 5 0 0 1 6 4.196"/></g></svg>
                  <div>Get AI Suggestions</div>
              </button>
              <button class="jp-Button2 apply-button">
                  <span class="material-icons">check</span>
                  <div>Apply</div>
              </button>
          </div>
        </div>
      `;
        // Apply Button
        const applyButton = this.node.querySelector('.apply-button');
        if (applyButton) {
            applyButton.addEventListener('click', () => {
                const textInput = this.node.querySelector('.jp-a11y-input');
                this.applyTextToCell(textInput.value.trim());
            });
        }
        // Suggest Button
        const suggestButton = this.node.querySelector('.suggest-button');
        suggestButton.style.display = aiEnabled ? 'flex' : 'none';
        if (suggestButton) {
            suggestButton.addEventListener('click', () => this.displayAISuggestions());
        }
    }
}
class ImageAltFixWidget extends TextFieldFixWidget {
    constructor(issue, cell, aiEnabled) {
        super(issue, cell, aiEnabled);
    }
    applyTextToCell(providedAltText) {
        if (providedAltText === '') {
            console.log('Empty alt text, returning');
            return;
        }
        const entireCellContent = this.cell.model.sharedModel.getSource();
        const target = this.issue.issueContentRaw;
        // Handle HTML image tags
        const handleHtmlImage = () => {
            // Alt attribute exists but is empty
            if (target.includes('alt=""') || target.includes("alt=''")) {
                return entireCellContent.replace(target, target.replace(/alt=["']\s*["']/, `alt="${providedAltText}"`));
            }
            // Alt attribute does not exist
            else {
                return entireCellContent.replace(target, target.replace(/>$/, ` alt="${providedAltText}">`));
            }
        };
        // Handle markdown images
        const handleMarkdownImage = () => {
            return entireCellContent.replace(target, target.replace(/!\[\]/, `![${providedAltText}]`));
        };
        let newContent = entireCellContent;
        if (target.startsWith('<img')) {
            newContent = handleHtmlImage();
        }
        else if (target.startsWith('![')) {
            newContent = handleMarkdownImage();
        }
        this.cell.model.sharedModel.setSource(newContent);
        // Remove the issue widget
        this.removeIssueWidget();
    }
    async displayAISuggestions() {
        console.log('Getting AI suggestions');
        const altTextInput = this.node.querySelector('.jp-a11y-input');
        if (!altTextInput) {
            return;
        }
        // Save the original placeholder text
        const originalPlaceholder = altTextInput.placeholder;
        // Create loading overlay (so we can see the loading state)
        const loadingOverlay = document.createElement('div');
        loadingOverlay.style.position = 'absolute';
        loadingOverlay.style.left = '8px'; // Matching input text padding
        loadingOverlay.style.top = '8px';
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.alignItems = 'center';
        loadingOverlay.style.gap = '8px';
        loadingOverlay.style.color = '#666';
        loadingOverlay.innerHTML = `
          <span class="material-icons loading">refresh</span>
          Getting AI suggestions...
      `;
        // Add relative positioning to input container and append loading overlay
        const inputContainer = altTextInput.parentElement;
        if (inputContainer) {
            inputContainer.style.position = 'relative';
            inputContainer.appendChild(loadingOverlay);
        }
        // Show loading state in the input
        altTextInput.disabled = true;
        altTextInput.style.color = 'transparent'; // Hide input text while loading
        altTextInput.placeholder = ''; // Clear placeholder while showing loading overlay
        try {
            const suggestion = await (0,_utils_ai_utils__WEBPACK_IMPORTED_MODULE_2__.getImageAltSuggestion)(this.issue, _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings().baseUrl + 'ollama/', 'mistral');
            if (suggestion !== 'Error') {
                // Extract alt text from the suggestion, handling both single and double quotes
                const altMatch = suggestion.match(/alt=['"]([^'"]*)['"]/);
                if (altMatch && altMatch[1]) {
                    altTextInput.value = altMatch[1];
                }
                else {
                    altTextInput.value = suggestion; // Fallback to full suggestion if no alt text found
                }
            }
            else {
                altTextInput.placeholder =
                    'Error getting suggestions. Please try again.';
            }
        }
        catch (error) {
            console.error(error);
            altTextInput.placeholder = 'Error getting suggestions. Please try again.';
        }
        finally {
            altTextInput.disabled = false;
            altTextInput.style.color = ''; // Restore text color
            loadingOverlay.remove(); // Remove loading overlay
            if (altTextInput.value) {
                altTextInput.placeholder = originalPlaceholder;
            }
        }
    }
}
class TableCaptionFixWidget extends TextFieldFixWidget {
    constructor(issue, cell, aiEnabled) {
        super(issue, cell, aiEnabled);
    }
    applyTextToCell(providedCaption) {
        if (providedCaption === '') {
            console.log('Empty caption text, returning');
            return;
        }
        const entireCellContent = this.cell.model.sharedModel.getSource();
        const target = this.issue.issueContentRaw;
        const handleHtmlTable = () => {
            // Check if table already has a caption
            if (target.includes('<caption>')) {
                return entireCellContent.replace(/<caption>.*?<\/caption>/, `<caption>${providedCaption}</caption>`);
            }
            else {
                return entireCellContent.replace(/<table[^>]*>/, `$&\n  <caption>${providedCaption}</caption>`);
            }
        };
        let newContent = entireCellContent;
        if (target.includes('<table')) {
            newContent = handleHtmlTable();
        }
        this.cell.model.sharedModel.setSource(newContent);
        // Remove the issue widget
        this.removeIssueWidget();
    }
    async displayAISuggestions() {
        console.log('Getting AI suggestions for table caption');
        const captionInput = this.node.querySelector('.jp-a11y-input');
        if (!captionInput) {
            return;
        }
        // Save the original placeholder text
        const originalPlaceholder = captionInput.placeholder;
        // Create loading overlay
        const loadingOverlay = document.createElement('div');
        loadingOverlay.style.position = 'absolute';
        loadingOverlay.style.left = '8px';
        loadingOverlay.style.top = '8px';
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.alignItems = 'center';
        loadingOverlay.style.gap = '8px';
        loadingOverlay.style.color = '#666';
        loadingOverlay.innerHTML = `
          <span class="material-icons loading">refresh</span>
          Getting AI suggestions...
      `;
        // Add relative positioning to input container and append loading overlay
        const inputContainer = captionInput.parentElement;
        if (inputContainer) {
            inputContainer.style.position = 'relative';
            inputContainer.appendChild(loadingOverlay);
        }
        // Show loading state in the input
        captionInput.disabled = true;
        captionInput.style.color = 'transparent';
        captionInput.placeholder = '';
        try {
            const suggestion = await (0,_utils_ai_utils__WEBPACK_IMPORTED_MODULE_2__.getTableCaptionSuggestion)(this.issue, _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings().baseUrl + 'ollama/', 'mistral');
            if (suggestion !== 'Error') {
                captionInput.value = suggestion;
            }
            else {
                captionInput.placeholder =
                    'Error getting suggestions. Please try again.';
            }
        }
        catch (error) {
            console.error(error);
            captionInput.placeholder = 'Error getting suggestions. Please try again.';
        }
        finally {
            captionInput.disabled = false;
            captionInput.style.color = '';
            loadingOverlay.remove();
            if (captionInput.value) {
                captionInput.placeholder = originalPlaceholder;
            }
        }
    }
}
// Dropdowns
class DropdownFixWidget extends FixWidget {
    constructor(issue, cell, aiEnabled) {
        super(issue, cell, aiEnabled);
        this.selectedOption = '';
        // Simplified DOM structure
        this.node.innerHTML = `
      <div class="table-header-fix-widget">
        <div class="custom-dropdown">
          <button class="dropdown-button">
            <span class="dropdown-text">Apply a table header</span>
            <svg class="dropdown-arrow" viewBox="0 0 24 24" width="24" height="24">
              <path fill="currentColor" d="M7 10l5 5 5-5z"/>
            </svg>
          </button>
          <div class="dropdown-content hidden">
            <div class="dropdown-option" data-value="first-row">
              The first row is a header
            </div>
            <div class="dropdown-option" data-value="first-column">
              The first column is a header
            </div>
            <div class="dropdown-option" data-value="both">
              The first row and column are headers
            </div>
          </div>
        </div>
        <button class="jp-Button2 apply-button">
            <span class="material-icons">check</span>
            <div>Apply</div>
          </button>
      </div>
    `;
        this.dropdownButton = this.node.querySelector('.dropdown-button');
        this.dropdownContent = this.node.querySelector('.dropdown-content');
        this.dropdownText = this.node.querySelector('.dropdown-text');
        this.applyButton = this.node.querySelector('.apply-button');
        // Setup dropdown handlers
        this.setupDropdownHandlers();
    }
    setupDropdownHandlers() {
        // Toggle dropdown
        this.dropdownButton.addEventListener('click', () => {
            this.dropdownContent.classList.toggle('hidden');
            this.dropdownButton.classList.toggle('active');
        });
        // Close dropdown when clicking outside
        document.addEventListener('click', event => {
            if (!this.node.contains(event.target)) {
                this.dropdownContent.classList.add('hidden');
                this.dropdownButton.classList.remove('active');
            }
        });
        // Option selection
        const options = this.node.querySelectorAll('.dropdown-option');
        options.forEach(option => {
            option.addEventListener('click', () => {
                var _a;
                const value = option.dataset.value || '';
                this.selectedOption = value;
                this.dropdownText.textContent = ((_a = option.textContent) === null || _a === void 0 ? void 0 : _a.trim()) || '';
                this.dropdownContent.classList.add('hidden');
                this.dropdownButton.classList.remove('active');
                this.applyButton.style.display = 'flex';
            });
        });
        // Apply button
        this.applyButton.addEventListener('click', () => {
            if (this.selectedOption) {
                this.applyDropdownSelection(this.selectedOption);
            }
        });
    }
}
class TableHeaderFixWidget extends DropdownFixWidget {
    constructor(issue, cell, aiEnabled) {
        super(issue, cell, aiEnabled);
    }
    applyDropdownSelection(headerType) {
        const entireCellContent = this.cell.model.sharedModel.getSource();
        const target = this.issue.issueContentRaw;
        const convertToHeaderCell = (cell) => {
            // Remove any existing th tags if present
            cell = cell.replace(/<\/?th[^>]*>/g, '');
            // Remove td tags if present
            cell = cell.replace(/<\/?td[^>]*>/g, '');
            // Wrap with th tags
            return `<th>${cell.trim()}</th>`;
        };
        const processTable = (tableHtml) => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(tableHtml, 'text/html');
            const table = doc.querySelector('table');
            if (!table) {
                return tableHtml;
            }
            // Get all rows, filtering out empty ones
            const rows = Array.from(table.querySelectorAll('tr')).filter(row => row.querySelectorAll('td, th').length > 0);
            if (rows.length === 0) {
                return tableHtml;
            }
            switch (headerType) {
                case 'first-row': {
                    // Convert first row cells to headers
                    const firstRow = rows[0];
                    const cells = Array.from(firstRow.querySelectorAll('td, th'));
                    cells.forEach(cell => {
                        const newHeader = convertToHeaderCell(cell.innerHTML);
                        cell.outerHTML = newHeader;
                    });
                    break;
                }
                case 'first-column': {
                    // Convert first column cells to headers
                    rows.forEach(row => {
                        const firstCell = row.querySelector('td, th');
                        if (firstCell) {
                            const newHeader = convertToHeaderCell(firstCell.innerHTML);
                            firstCell.outerHTML = newHeader;
                        }
                    });
                    break;
                }
                case 'both': {
                    // Convert both first row and first column
                    rows.forEach((row, rowIndex) => {
                        const cells = Array.from(row.querySelectorAll('td, th'));
                        cells.forEach((cell, cellIndex) => {
                            if (rowIndex === 0 || cellIndex === 0) {
                                const newHeader = convertToHeaderCell(cell.innerHTML);
                                cell.outerHTML = newHeader;
                            }
                        });
                    });
                    break;
                }
            }
            return table.outerHTML;
        };
        const newContent = entireCellContent.replace(target, processTable(target));
        this.cell.model.sharedModel.setSource(newContent);
        this.removeIssueWidget();
    }
}


/***/ }),

/***/ "./lib/components/IssueWidget.js":
/*!***************************************!*\
  !*** ./lib/components/IssueWidget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellIssueWidget: () => (/* binding */ CellIssueWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _FixWidget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./FixWidget */ "./lib/components/FixWidget.js");


class CellIssueWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(issue, cell, aiEnabled) {
        var _a;
        super();
        this.aiEnabled = false; // TODO: Create a higher order component to handle this
        this.issue = issue;
        this.cell = cell;
        this.aiEnabled = aiEnabled;
        this.addClass('issue-widget');
        this.node.innerHTML = `
      <button class="issue-header-button">
          <h3 class="issue-header">Issue: ${issue.violation.id} <span class="chevron material-icons">expand_more</span></h3>
      </button>
      <div class="collapsible-content" style="display: none;">
          <p class="description">
              ${issue.violation.description} <a href="${issue.violation.descriptionUrl}" target="_blank">(learn more about the issue)</a>.
          </p>
          <div class="button-container">
              <button class="jp-Button2 locate-button">
                  <span class="material-icons">search</span>
                  <div>Locate</div>
              </button>
          </div>
          <div class="fix-widget-container"></div>
      </div>
    `;
        // Add event listeners using query selectors
        const headerButton = this.node.querySelector('.issue-header-button');
        const collapsibleContent = this.node.querySelector('.collapsible-content');
        // Toggle collapsible content when header is clicked
        headerButton === null || headerButton === void 0 ? void 0 : headerButton.addEventListener('click', () => {
            if (collapsibleContent) {
                const isHidden = collapsibleContent.style.display === 'none';
                collapsibleContent.style.display = isHidden ? 'block' : 'none';
                const expandIcon = this.node.querySelector('.chevron');
                expandIcon === null || expandIcon === void 0 ? void 0 : expandIcon.classList.toggle('expanded');
            }
        });
        const locateButton = this.node.querySelector('.locate-button');
        locateButton === null || locateButton === void 0 ? void 0 : locateButton.addEventListener('click', () => this.navigateToCell());
        // Show suggest button initially if AI is enabled
        const mainPanel = document.getElementById('a11y-sidebar');
        if (mainPanel) {
            const aiToggleButton = mainPanel.querySelector('.ai-control-button');
            if (aiToggleButton && ((_a = aiToggleButton.textContent) === null || _a === void 0 ? void 0 : _a.includes('Enabled'))) {
                this.aiEnabled = true;
            }
            else {
                this.aiEnabled = false;
            }
        }
        // Dynamically add the TextFieldFixWidget if needed
        const fixWidgetContainer = this.node.querySelector('.fix-widget-container');
        if (!fixWidgetContainer) {
            return;
        }
        if (this.issue.violation.id === 'image-alt') {
            const textFieldFixWidget = new _FixWidget__WEBPACK_IMPORTED_MODULE_1__.ImageAltFixWidget(this.issue, this.cell, this.aiEnabled);
            fixWidgetContainer.appendChild(textFieldFixWidget.node);
        }
        else if (this.issue.violation.id === 'table-has-caption') {
            console.log('Table caption issue');
            const tableCaptionFixWidget = new _FixWidget__WEBPACK_IMPORTED_MODULE_1__.TableCaptionFixWidget(this.issue, this.cell, this.aiEnabled);
            fixWidgetContainer.appendChild(tableCaptionFixWidget.node);
        }
        else if (this.issue.violation.id === 'td-has-header') {
            const tableHeaderFixWidget = new _FixWidget__WEBPACK_IMPORTED_MODULE_1__.TableHeaderFixWidget(this.issue, this.cell, this.aiEnabled);
            fixWidgetContainer.appendChild(tableHeaderFixWidget.node);
        }
    }
    navigateToCell() {
        this.cell.node.scrollIntoView({ behavior: 'auto', block: 'nearest' });
        requestAnimationFrame(() => {
            this.cell.node.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        this.cell.node.style.transition = 'background-color 0.5s ease';
        this.cell.node.style.backgroundColor = '#DB3939';
        setTimeout(() => {
            this.cell.node.style.backgroundColor = '';
        }, 1000);
    }
}


/***/ }),

/***/ "./lib/components/MainPanelWidget.js":
/*!*******************************************!*\
  !*** ./lib/components/MainPanelWidget.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MainPanelWidget: () => (/* binding */ MainPanelWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _IssueWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./IssueWidget */ "./lib/components/IssueWidget.js");
/* harmony import */ var _utils_metadata__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils/metadata */ "./lib/utils/metadata.js");
/* harmony import */ var _utils_detection_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils/detection-utils */ "./lib/utils/detection-utils.js");
/* harmony import */ var _utils_ai_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils/ai-utils */ "./lib/utils/ai-utils.js");







class MainPanelWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.modelPulled = false;
        this.aiEnabled = false;
        this.currentNotebook = null;
        this.addClass('a11y-panel');
        this.id = 'a11y-sidebar';
        const accessibilityIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
            name: 'a11y:accessibility',
            svgstr: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#154F92" d="M256 48c114.953 0 208 93.029 208 208 0 114.953-93.029 208-208 208-114.953 0-208-93.029-208-208 0-114.953 93.029-208 208-208m0-40C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 56C149.961 64 64 149.961 64 256s85.961 192 192 192 192-85.961 192-192S362.039 64 256 64zm0 44c19.882 0 36 16.118 36 36s-16.118 36-36 36-36-16.118-36-36 16.118-36 36-36zm117.741 98.023c-28.712 6.779-55.511 12.748-82.14 15.807.851 101.023 12.306 123.052 25.037 155.621 3.617 9.26-.957 19.698-10.217 23.315-9.261 3.617-19.699-.957-23.316-10.217-8.705-22.308-17.086-40.636-22.261-78.549h-9.686c-5.167 37.851-13.534 56.208-22.262 78.549-3.615 9.255-14.05 13.836-23.315 10.217-9.26-3.617-13.834-14.056-10.217-23.315 12.713-32.541 24.185-54.541 25.037-155.621-26.629-3.058-53.428-9.027-82.141-15.807-8.6-2.031-13.926-10.648-11.895-19.249s10.647-13.926 19.249-11.895c96.686 22.829 124.283 22.783 220.775 0 8.599-2.03 17.218 3.294 19.249 11.895 2.029 8.601-3.297 17.219-11.897 19.249z"/></svg>'
        });
        this.title.icon = accessibilityIcon;
        this.node.innerHTML = `
      <div class="main-container">
          <div class="notice-container">
              <div class="notice-header">
                  <div class="notice-title">
                      <span class="chevron material-icons">expand_more</span>
                      <strong>Notice: Known cell navigation error </strong>
                  </div>
                  <button class="notice-delete-button">✕</button>
              </div>
              <div class="notice-content hidden">
                  <p>
                      The jupyterlab-a11y-checker has a known cell navigation issue for Jupyterlab version 4.2.5 or later. 
                      To fix this, please navigate to 'Settings' → 'Settings Editor' → Notebook, scroll down to 'Windowing mode', 
                      and choose 'defer' from the dropdown. Please note that this option may reduce the performance of the application. 
                      For more information, please see the <a href="https://jupyter-notebook.readthedocs.io/en/stable/changelog.html" target="_blank" style="text-decoration: underline;">Jupyter Notebook changelog.</a>
                  </p>
              </div>
          </div>
          <h1 class="main-title">Accessibility Checker</h1>
          <div class="controls-container">
              <button class="control-button ai-control-button">
                <span class="material-icons">auto_awesome</span>
                Use AI : Disabled
              </button>
              <button class="control-button analyze-control-button">
                <span class="material-icons">science</span>  
                Analyze Notebook
              </button>
          </div>
          <div class="issues-container"></div>
      </div>
        `;
        // Notice
        const noticeContainer = this.node.querySelector('.notice-container');
        const noticeContent = this.node.querySelector('.notice-content');
        const noticeToggleButton = this.node.querySelector('.notice-title');
        const noticeDeleteButton = this.node.querySelector('.notice-delete-button');
        const expandIcon = this.node.querySelector('.chevron');
        noticeToggleButton === null || noticeToggleButton === void 0 ? void 0 : noticeToggleButton.addEventListener('click', () => {
            noticeContent === null || noticeContent === void 0 ? void 0 : noticeContent.classList.toggle('hidden');
            expandIcon === null || expandIcon === void 0 ? void 0 : expandIcon.classList.toggle('expanded');
        });
        noticeDeleteButton === null || noticeDeleteButton === void 0 ? void 0 : noticeDeleteButton.addEventListener('click', () => {
            noticeContainer === null || noticeContainer === void 0 ? void 0 : noticeContainer.classList.add('hidden');
        });
        // Controls
        const aiControlButton = this.node.querySelector('.ai-control-button');
        const analyzeControlButton = this.node.querySelector('.analyze-control-button');
        const progressIcon = `
    <svg class="icon loading" viewBox="0 0 24 24">
        <path d="M12 4V2C6.48 2 2 6.48 2 12h2c0-4.41 3.59-8 8-8z"/>
    </svg>
    `;
        aiControlButton === null || aiControlButton === void 0 ? void 0 : aiControlButton.addEventListener('click', async () => {
            const aiIcon = '<span class="material-icons">auto_awesome</span>';
            // First Time Enabling AI
            if (!this.aiEnabled && !this.modelPulled) {
                aiControlButton.innerHTML = `${progressIcon} Please wait...`;
                aiControlButton.disabled = true;
                try {
                    const SERVER_URL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl() + 'ollama/';
                    await (0,_utils_ai_utils__WEBPACK_IMPORTED_MODULE_3__.pullOllamaModel)(SERVER_URL, 'mistral');
                    this.modelPulled = true;
                    this.aiEnabled = true;
                }
                catch (error) {
                    console.error('Failed to pull model:', error);
                }
                finally {
                    aiControlButton.innerHTML = `${aiIcon} Use AI : ${this.modelPulled ? 'Enabled' : 'Failed'}`;
                    aiControlButton.disabled = false;
                }
            }
            // Toggle Use AI State
            else {
                this.aiEnabled = !this.aiEnabled;
                aiControlButton.innerHTML = `${aiIcon} Use AI : ${this.aiEnabled ? 'Enabled' : 'Disabled'}`;
            }
            // Update every ai suggestion button visibility
            const suggestButtons = this.node.querySelectorAll('.suggest-button');
            suggestButtons.forEach(button => {
                button.style.display = this.aiEnabled
                    ? 'flex'
                    : 'none';
            });
        });
        analyzeControlButton === null || analyzeControlButton === void 0 ? void 0 : analyzeControlButton.addEventListener('click', async () => {
            if (!this.currentNotebook) {
                console.log('No current notebook found');
                return;
            }
            const analyzeControlButtonText = analyzeControlButton.innerHTML;
            const issuesContainer = this.node.querySelector('.issues-container');
            issuesContainer.innerHTML = '';
            analyzeControlButton.innerHTML = `${progressIcon} Please wait...`;
            analyzeControlButton.disabled = true;
            try {
                // Identify issues
                const notebookIssues = await (0,_utils_detection_utils__WEBPACK_IMPORTED_MODULE_4__.analyzeCellsAccessibility)(this.currentNotebook);
                if (notebookIssues.length === 0) {
                    issuesContainer.innerHTML =
                        '<div class="no-issues">No issues found</div>';
                    return;
                }
                // Group issues by category
                const issuesByCategory = new Map();
                notebookIssues.forEach(notebookIssue => {
                    const categoryName = _utils_metadata__WEBPACK_IMPORTED_MODULE_5__.issueToCategory.get(notebookIssue.violation.id) || 'Other';
                    if (!issuesByCategory.has(categoryName)) {
                        issuesByCategory.set(categoryName, []);
                    }
                    issuesByCategory.get(categoryName).push(notebookIssue);
                });
                // Create widgets for each category
                for (const categoryName of _utils_metadata__WEBPACK_IMPORTED_MODULE_5__.issueCategoryNames) {
                    const categoryIssues = issuesByCategory.get(categoryName) || [];
                    if (categoryIssues.length === 0) {
                        continue;
                    }
                    const categoryWidget = document.createElement('div');
                    categoryWidget.classList.add('category');
                    categoryWidget.innerHTML = `
            <h2 class="category-title">${categoryName}</h2>
            <hr>
            <div class="issues-list"></div>
          `;
                    const issuesContainer = this.node.querySelector('.issues-container');
                    issuesContainer.appendChild(categoryWidget);
                    const issuesList = categoryWidget.querySelector('.issues-list');
                    categoryIssues.forEach(issue => {
                        const issueWidget = new _IssueWidget__WEBPACK_IMPORTED_MODULE_6__.CellIssueWidget(issue, this.currentNotebook.content.widgets[issue.cellIndex], this.aiEnabled);
                        issuesList.appendChild(issueWidget.node);
                    });
                }
            }
            catch (error) {
                issuesContainer.innerHTML = '';
                console.error('Error analyzing notebook:', error);
            }
            finally {
                analyzeControlButton.innerHTML = analyzeControlButtonText;
                analyzeControlButton.disabled = false;
            }
        });
    }
    setNotebook(notebook) {
        this.currentNotebook = notebook;
        const issuesContainer = this.node.querySelector('.issues-container');
        issuesContainer.innerHTML = '';
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_MainPanelWidget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/MainPanelWidget */ "./lib/components/MainPanelWidget.js");



const extension = {
    id: 'jupyterlab-a11y-fix',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    activate: (app, labShell) => {
        const panel = new _components_MainPanelWidget__WEBPACK_IMPORTED_MODULE_2__.MainPanelWidget();
        labShell.add(panel, 'right');
        // Update current notebook when active widget changes
        labShell.currentChanged.connect(() => {
            const current = labShell.currentWidget;
            if (current instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel) {
                panel.setNotebook(current);
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/utils/ai-utils.js":
/*!*******************************!*\
  !*** ./lib/utils/ai-utils.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   formatPrompt: () => (/* binding */ formatPrompt),
/* harmony export */   getFixSuggestions: () => (/* binding */ getFixSuggestions),
/* harmony export */   getImageAltSuggestion: () => (/* binding */ getImageAltSuggestion),
/* harmony export */   getTableCaptionSuggestion: () => (/* binding */ getTableCaptionSuggestion),
/* harmony export */   pullOllamaModel: () => (/* binding */ pullOllamaModel)
/* harmony export */ });
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_0__);

function formatPrompt(issue) {
    let prompt = 'The following represents a jupyter notebook cell and a accessibility issue found in it.\n\n';
    const cellIssue = issue;
    prompt += `Content: \n${cellIssue.issueContentRaw}\n\n`;
    prompt += `Issue: ${cellIssue.violation.id}\n\n`;
    prompt += `Description: ${cellIssue.violation.description}\n\n`;
    prompt += `Respond in JSON format with the following fields:
    - exampleCellContent: A suggested fix for the cell, without any explanation.
    `;
    return prompt;
}
async function getFixSuggestions(prompt, userURL, modelName) {
    try {
        const body = JSON.stringify({
            model: modelName,
            prompt: prompt,
            stream: false
        });
        const response = await axios__WEBPACK_IMPORTED_MODULE_0___default().post(userURL + 'api/generate', body, {
            headers: { 'Content-Type': 'application/json' }
        });
        const responseText = await response.data.response.trim();
        const responseObj = JSON.parse(responseText);
        console.log(responseText);
        try {
            return responseObj.exampleCellContent;
        }
        catch (e) {
            console.error('Failed to parse suggestion:', e);
            return 'Invalid response format';
        }
    }
    catch (error) {
        console.error('Error getting suggestions:', error);
        return 'Error';
    }
}
async function getImageAltSuggestion(issue, userURL, modelName) {
    let prompt = 'Given the following code, read the image url and respond with a short description of the image, without any explanation.';
    prompt += `Content: \n${issue.issueContentRaw}\n\n`;
    try {
        const body = JSON.stringify({
            model: modelName,
            prompt: prompt,
            stream: false
        });
        const response = await axios__WEBPACK_IMPORTED_MODULE_0___default().post(userURL + 'api/generate', body, {
            headers: { 'Content-Type': 'application/json' }
        });
        const responseText = await response.data.response.trim();
        return responseText;
    }
    catch (error) {
        console.error('Error getting suggestions:', error);
        return 'Error';
    }
}
async function getTableCaptionSuggestion(issue, userURL, modelName) {
    const prompt = `Given this HTML table, please respond with a short description of the table, without any explanation. Here's the table:
    ${issue.issueContentRaw}`;
    try {
        const body = JSON.stringify({
            model: modelName,
            prompt: prompt,
            stream: false
        });
        const response = await axios__WEBPACK_IMPORTED_MODULE_0___default().post(userURL + 'api/generate', body, {
            headers: { 'Content-Type': 'application/json' }
        });
        const responseText = await response.data.response.trim();
        return responseText;
    }
    catch (error) {
        console.error('Error getting suggestions:', error);
        return 'Error';
    }
}
async function pullOllamaModel(userURL, modelName) {
    try {
        const payload = {
            name: modelName,
            stream: false,
            options: {
                low_cpu_mem_usage: true,
                use_fast_tokenizer: true
            }
        };
        // Instead of aborting, let's just monitor the time
        console.log('Starting model pull...');
        const response = await axios__WEBPACK_IMPORTED_MODULE_0___default().post(userURL + 'api/pull', payload, {
            headers: { 'Content-Type': 'application/json' }
        });
        if (response.status !== 200) {
            throw new Error('Failed to pull model');
        }
    }
    catch (error) {
        console.error('Error pulling model:', error);
        throw error;
    }
}


/***/ }),

/***/ "./lib/utils/detection-utils.js":
/*!**************************************!*\
  !*** ./lib/utils/detection-utils.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   analyzeCellsAccessibility: () => (/* binding */ analyzeCellsAccessibility)
/* harmony export */ });
/* harmony import */ var axe_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! axe-core */ "webpack/sharing/consume/default/axe-core/axe-core");
/* harmony import */ var axe_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(axe_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var marked__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! marked */ "webpack/sharing/consume/default/marked/marked");
/* harmony import */ var marked__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(marked__WEBPACK_IMPORTED_MODULE_1__);


async function analyzeCellsAccessibility(panel) {
    const notebookIssues = [];
    const tempDiv = document.createElement('div');
    document.body.appendChild(tempDiv);
    const axeConfig = {
        runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']
    };
    try {
        const cells = panel.content.widgets;
        for (let i = 0; i < cells.length; i++) {
            const cell = cells[i];
            if (!cell || !cell.model) {
                console.warn(`Skipping cell ${i}: Invalid cell or model`);
                continue;
            }
            const cellType = cell.model.type;
            if (cellType === 'markdown') {
                const rawMarkdown = cell.model.sharedModel.getSource();
                if (rawMarkdown.trim()) {
                    tempDiv.innerHTML = await marked__WEBPACK_IMPORTED_MODULE_1__.marked.parse(rawMarkdown);
                    const results = await axe_core__WEBPACK_IMPORTED_MODULE_0___default().run(tempDiv, axeConfig);
                    const violations = results.violations;
                    // Can have multiple violations in a single cell
                    if (violations.length > 0) {
                        violations.forEach(violation => {
                            violation.nodes.forEach(node => {
                                notebookIssues.push({
                                    cellIndex: i,
                                    cellType: cellType,
                                    violation: {
                                        id: violation.id,
                                        description: violation.description,
                                        descriptionUrl: violation.helpUrl
                                    },
                                    issueContentRaw: node.html
                                });
                            });
                        });
                    }
                    // Add custom image issue detection
                    notebookIssues.push(...detectImageIssuesInCell(rawMarkdown, i, cellType));
                    notebookIssues.push(...detectTableIssuesInCell(rawMarkdown, i, cellType));
                }
            }
            else if (cellType === 'code') {
                const codeInput = cell.node.querySelector('.jp-InputArea-editor');
                const codeOutput = cell.node.querySelector('.jp-OutputArea');
                if (codeInput || codeOutput) {
                    // We would have to feed this into a language model to get the suggested fix.
                }
            }
        }
    }
    finally {
        tempDiv.remove();
    }
    return notebookIssues;
}
// Image
function detectImageIssuesInCell(rawMarkdown, cellIndex, cellType) {
    const notebookIssues = [];
    // Check for images without alt text in markdown syntax
    const mdSyntaxMissingAltRegex = /!\[\]\([^)]+\)/g;
    // Check for images without alt tag or empty alt tag in HTML syntax
    const htmlSyntaxMissingAltRegex = /<img[^>]*alt=""[^>]*>/g;
    let match;
    while ((match = mdSyntaxMissingAltRegex.exec(rawMarkdown)) !== null ||
        (match = htmlSyntaxMissingAltRegex.exec(rawMarkdown)) !== null) {
        notebookIssues.push({
            cellIndex,
            cellType: cellType,
            violation: {
                id: 'image-alt',
                description: 'Images must have alternate text',
                descriptionUrl: 'https://dequeuniversity.com/rules/axe/4.7/image-alt'
            },
            issueContentRaw: match[0]
        });
    }
    return notebookIssues;
}
// Table
function detectTableIssuesInCell(rawMarkdown, cellIndex, cellType) {
    const notebookIssues = [];
    // Check for tables without th tags
    const tableWithoutThRegex = /<table[^>]*>(?![\s\S]*?<th[^>]*>)[\s\S]*?<\/table>/gi;
    let match;
    while ((match = tableWithoutThRegex.exec(rawMarkdown)) !== null) {
        notebookIssues.push({
            cellIndex,
            cellType: cellType,
            violation: {
                id: 'td-has-header',
                description: 'Tables must have header information',
                descriptionUrl: 'https://dequeuniversity.com/rules/axe/4.10/td-has-header?application=RuleDescription'
            },
            issueContentRaw: match[0]
        });
    }
    // Check for tables without caption tags
    const tableWithoutCaptionRegex = /<table[^>]*>(?![\s\S]*?<caption[^>]*>)[\s\S]*?<\/table>/gi;
    while ((match = tableWithoutCaptionRegex.exec(rawMarkdown)) !== null) {
        notebookIssues.push({
            cellIndex,
            cellType: cellType,
            violation: {
                id: 'table-has-caption',
                description: 'Tables must have caption information',
                descriptionUrl: ''
            },
            issueContentRaw: match[0]
        });
    }
    return notebookIssues;
}
// TODO: Headings
// TODO: Color
// TODO: Links
// TODO: Other


/***/ }),

/***/ "./lib/utils/metadata.js":
/*!*******************************!*\
  !*** ./lib/utils/metadata.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   issueCategoryNames: () => (/* binding */ issueCategoryNames),
/* harmony export */   issueToCategory: () => (/* binding */ issueToCategory)
/* harmony export */ });
const issueCategoryNames = [
    'Images',
    'Headings',
    'Lists',
    'Tables',
    'Color',
    'Links',
    'Other'
];
const issueToCategory = new Map([
    // 1. Images
    ['image-alt', 'Images'],
    // TODO: 2. Headings
    ['page-has-heading-one', 'Headings'],
    ['heading-order', 'Headings'],
    // TODO: 3. Lists
    // TODO: 4. Tables
    ['td-has-header', 'Tables'],
    ['table-has-caption', 'Tables']
    // TODO: 5. Color
    // TODO: 6. Links
    // TODO: 7. Other
]);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.92064af809126a68f295.js.map