"use strict";
(self["webpackChunka11y_checker"] = self["webpackChunka11y_checker"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.push([module.id, "@import url(https://fonts.googleapis.com/icon?family=Material+Icons);"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/* Import Material Icons */

/* Main Panel Layout */
.a11y-panel {
    background-color: white;
    height: 100%;
    overflow-y: auto;
}

.a11y-panel .main-container {
    padding: 0;
}

/* Notice Section */
.notice-container {
    background-color: #2c5282;
    color: white;
    overflow: hidden;
    padding: 8px 12px;
}

.notice-header {
    padding: 6px 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.notice-title {
    display: flex;
    align-items: center;
    gap: 8px;
}

.triangle {
    font-size: 12px;
}

.notice-delete-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 16px;
    padding: 4px;
}

.notice-content {
    padding: 8px 20px;
}

/* Main Title */
.main-title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin: 24px 4px;
}

/* Controls Section */
.controls-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 0 16px;
    margin-bottom: 24px;
}

.control-button {
    background-color: #2c5282;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 12px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 60%;
}

.control-button svg {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
}

.control-button div {
    text-align: left;
    flex: 1;
}

.control-button:hover {
    background-color: #2a4365;
}

/* Categories Section */
.issues-container {
    padding: 0 16px;
}

.no-issues {
    text-align: center;
    color: #666;
    padding: 24px;
}

.category {
    margin-bottom: 24px;
}

.category-title {
    font-size: 20px;
    margin-bottom: 8px;
}

.category hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 0 0 16px 0;
}

.issues-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* Issue Widget */
.issue-widget {
    margin: 5px 0;
    margin-left: 12px;
}

.issue-widget .container {
    display: flex;
    flex-direction: column;
}

.issue-widget .issue-header-button {
    background: none;
    border: none;
    padding: 0;
    text-align: left;
    cursor: pointer;
    margin-bottom: 8px;
}

.issue-widget .issue-header {
    font-size: 16px;
    font-weight: 700;
    margin: 0;
    color: #000;
    display: flex;
    align-items: center;
    gap: 4px;
}

.issue-widget .description {
    margin: 0 0 12px 0;
    font-size: 14px;
}

.issue-widget .description a {
    color: inherit;
    text-decoration: underline;
}

/* Button Styles */
.issue-widget .button-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
}

.issue-widget .jp-Button {
    background-color: #2c5282;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    width: 60%;
    justify-content: flex-start;
    gap: 8px;
}

.jp-Button2 {
    background-color: #2c5282;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    width: 50%;
    gap: 8px;
    display: flex;
    flex-direction: row;
    align-items: center;
}

.issue-widget .jp-Button:hover {
    background-color: #2a4365;
}

.issue-widget .apply-button {
    margin-top: 8px;
    background-color: #2c5282;
    margin-left: auto;
    display: flex;
    width: auto !important;
}

/* Suggestion Styles */
.issue-widget .suggestion-container {
    margin-bottom: 12px;
    margin-left: 30px;
    padding: 12px;
    background-color: #1a1a1a;
    border-radius: 4px;
    color: white;
    font-family: monospace;
}

.issue-widget .suggestion {
    word-wrap: break-word;
    white-space: pre-wrap;
}

.issue-widget .textfield-fix-widget {
    margin-bottom: 12px;
    margin-left: 30px;
    padding: 12px;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.textfield-fix-widget {
    background-color: #DCDCDC;
    padding: 12px;
    border-radius: 8px;
    margin-top: 12px;
    border: 1px solid black;
    min-width: 145px;
}

.jp-a11y-input {
    width: calc(100% - 16px);
    padding: 8px;
    margin-bottom: 8px;
    background-color: #DCDCDC;
    color: black;
    font-family: Inter, sans-serif;
    box-sizing: border-box;
    border: none;
    outline: none;
}

.textfield-buttons {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    flex-wrap: wrap;
    width: 100%;
    box-sizing: border-box;
}

/* Collapsible Content */
.collapsible-content {
    padding-left: 16px;
}

/* Icon Styles */
.icon {
    width: 18px;
    height: 18px;
    fill: currentColor;
}

.chevron {
    transition: transform 0.3s ease;
    transform-origin: center center;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    line-height: 1;
}

.chevron.expanded {
    transform: rotate(180deg);
}

.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.locate-button:hover {
    background-color: #2a4365;
}

.suggest-button,
.locate-button {
    background-color: #2C5B8E;
    color: white;
    font-family: Inter, sans-serif;
    flex: 0 0 auto;
    min-width: 140px;
    white-space: normal;
    word-wrap: break-word;
}

.apply-alt-button {
    background-color: #2C5B8E;
    color: white;
    font-family: Inter, sans-serif;
    flex: 0 0 auto;
    min-width: 90px;
    white-space: normal;
    word-wrap: break-word;
    max-width: 25%;
}

.suggest-button div,
.apply-alt-button div,
.locate-button div {
    text-align: left;
    flex: 1;
}

.suggest-button svg,
.apply-alt-button svg,
.locate-button svg {
    flex-shrink: 0;
}

.suggest-button {
    max-width: 60%;
}

.suggest-button:hover {
    background-color: #2a4365;
}

.apply-alt-button:hover {
    background-color: #2a4365;
}

/* Material Icons Styles */
.material-icons {
    font-family: 'Material Icons';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    /* Preferred icon size */
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    vertical-align: middle;
}

/* Icon sizes */
.material-icons.md-18 {
    font-size: 18px;
}

.material-icons.md-24 {
    font-size: 24px;
}

.material-icons.md-36 {
    font-size: 36px;
}

.material-icons.md-48 {
    font-size: 48px;
}

/* Icon colors */
.material-icons.md-dark {
    color: rgba(0, 0, 0, 0.54);
}

.material-icons.md-dark.md-inactive {
    color: rgba(0, 0, 0, 0.26);
}

.material-icons.md-light {
    color: rgba(255, 255, 255, 1);
}

.material-icons.md-light.md-inactive {
    color: rgba(255, 255, 255, 0.3);
}

/* Loading animation for Material Icons */
.material-icons.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.hidden:not(.dropdown-content) {
    display: none;
}

.table-header-fix-widget {
    margin-top: 8px;
}

.table-header-fix-widget .button-container {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}

.custom-dropdown {
    position: relative;
    width: calc(100% - 16px);
    margin-bottom: 8px;
    z-index: 9999;
    isolation: isolate;
}

.dropdown-button {
    width: 100%;
    padding: 8px 12px;
    background-color: white;
    color: black;
    border: 1px solid black;
    border-radius: 4px;
    cursor: pointer;
    font-family: Inter, sans-serif;
    font-size: 14px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.dropdown-button:hover {
    background-color: #2a4365;
    color: white;
}

.dropdown-button.active {
    background-color: #2a4365;
    color: white;
}

.dropdown-text {
    flex: 1;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.dropdown-arrow {
    margin-left: 8px;
    flex-shrink: 0;
}

.dropdown-content {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: white;
    border: 1px solid black;
    border-radius: 4px;
    margin-top: 4px;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dropdown-content.hidden {
    display: none;
}

.dropdown-option {
    padding: 8px 12px;
    cursor: pointer;
}

.dropdown-option:hover {
    background-color: #2a4365;
    color: white;
}

.table-header-fix-widget {
    margin-top: 8px;
}

.table-header-fix-widget .button-container {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/* Import Material Icons */\n@import url('https://fonts.googleapis.com/icon?family=Material+Icons');\n\n/* Main Panel Layout */\n.a11y-panel {\n    background-color: white;\n    height: 100%;\n    overflow-y: auto;\n}\n\n.a11y-panel .main-container {\n    padding: 0;\n}\n\n/* Notice Section */\n.notice-container {\n    background-color: #2c5282;\n    color: white;\n    overflow: hidden;\n    padding: 8px 12px;\n}\n\n.notice-header {\n    padding: 6px 8px;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}\n\n.notice-title {\n    display: flex;\n    align-items: center;\n    gap: 8px;\n}\n\n.triangle {\n    font-size: 12px;\n}\n\n.notice-delete-button {\n    background: none;\n    border: none;\n    color: white;\n    cursor: pointer;\n    font-size: 16px;\n    padding: 4px;\n}\n\n.notice-content {\n    padding: 8px 20px;\n}\n\n/* Main Title */\n.main-title {\n    font-size: 24px;\n    font-weight: bold;\n    text-align: center;\n    margin: 24px 4px;\n}\n\n/* Controls Section */\n.controls-container {\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    gap: 12px;\n    padding: 0 16px;\n    margin-bottom: 24px;\n}\n\n.control-button {\n    background-color: #2c5282;\n    color: white;\n    border: none;\n    border-radius: 4px;\n    padding: 12px;\n    font-size: 16px;\n    cursor: pointer;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    gap: 8px;\n    width: 60%;\n}\n\n.control-button svg {\n    flex-shrink: 0;\n    width: 24px;\n    height: 24px;\n}\n\n.control-button div {\n    text-align: left;\n    flex: 1;\n}\n\n.control-button:hover {\n    background-color: #2a4365;\n}\n\n/* Categories Section */\n.issues-container {\n    padding: 0 16px;\n}\n\n.no-issues {\n    text-align: center;\n    color: #666;\n    padding: 24px;\n}\n\n.category {\n    margin-bottom: 24px;\n}\n\n.category-title {\n    font-size: 20px;\n    margin-bottom: 8px;\n}\n\n.category hr {\n    border: none;\n    border-top: 1px solid #ddd;\n    margin: 0 0 16px 0;\n}\n\n.issues-list {\n    display: flex;\n    flex-direction: column;\n    gap: 12px;\n}\n\n/* Issue Widget */\n.issue-widget {\n    margin: 5px 0;\n    margin-left: 12px;\n}\n\n.issue-widget .container {\n    display: flex;\n    flex-direction: column;\n}\n\n.issue-widget .issue-header-button {\n    background: none;\n    border: none;\n    padding: 0;\n    text-align: left;\n    cursor: pointer;\n    margin-bottom: 8px;\n}\n\n.issue-widget .issue-header {\n    font-size: 16px;\n    font-weight: 700;\n    margin: 0;\n    color: #000;\n    display: flex;\n    align-items: center;\n    gap: 4px;\n}\n\n.issue-widget .description {\n    margin: 0 0 12px 0;\n    font-size: 14px;\n}\n\n.issue-widget .description a {\n    color: inherit;\n    text-decoration: underline;\n}\n\n/* Button Styles */\n.issue-widget .button-container {\n    display: flex;\n    flex-direction: column;\n    gap: 8px;\n    margin-bottom: 12px;\n}\n\n.issue-widget .jp-Button {\n    background-color: #2c5282;\n    color: white;\n    border: none;\n    border-radius: 4px;\n    padding: 8px 16px;\n    cursor: pointer;\n    font-size: 14px;\n    display: flex;\n    align-items: center;\n    width: 60%;\n    justify-content: flex-start;\n    gap: 8px;\n}\n\n.jp-Button2 {\n    background-color: #2c5282;\n    color: white;\n    border: none;\n    border-radius: 4px;\n    padding: 8px 16px;\n    cursor: pointer;\n    font-size: 14px;\n    width: 50%;\n    gap: 8px;\n    display: flex;\n    flex-direction: row;\n    align-items: center;\n}\n\n.issue-widget .jp-Button:hover {\n    background-color: #2a4365;\n}\n\n.issue-widget .apply-button {\n    margin-top: 8px;\n    background-color: #2c5282;\n    margin-left: auto;\n    display: flex;\n    width: auto !important;\n}\n\n/* Suggestion Styles */\n.issue-widget .suggestion-container {\n    margin-bottom: 12px;\n    margin-left: 30px;\n    padding: 12px;\n    background-color: #1a1a1a;\n    border-radius: 4px;\n    color: white;\n    font-family: monospace;\n}\n\n.issue-widget .suggestion {\n    word-wrap: break-word;\n    white-space: pre-wrap;\n}\n\n.issue-widget .textfield-fix-widget {\n    margin-bottom: 12px;\n    margin-left: 30px;\n    padding: 12px;\n    border-radius: 4px;\n    display: flex;\n    flex-direction: column;\n    gap: 8px;\n}\n\n.textfield-fix-widget {\n    background-color: #DCDCDC;\n    padding: 12px;\n    border-radius: 8px;\n    margin-top: 12px;\n    border: 1px solid black;\n    min-width: 145px;\n}\n\n.jp-a11y-input {\n    width: calc(100% - 16px);\n    padding: 8px;\n    margin-bottom: 8px;\n    background-color: #DCDCDC;\n    color: black;\n    font-family: Inter, sans-serif;\n    box-sizing: border-box;\n    border: none;\n    outline: none;\n}\n\n.textfield-buttons {\n    display: flex;\n    gap: 8px;\n    justify-content: flex-end;\n    flex-wrap: wrap;\n    width: 100%;\n    box-sizing: border-box;\n}\n\n/* Collapsible Content */\n.collapsible-content {\n    padding-left: 16px;\n}\n\n/* Icon Styles */\n.icon {\n    width: 18px;\n    height: 18px;\n    fill: currentColor;\n}\n\n.chevron {\n    transition: transform 0.3s ease;\n    transform-origin: center center;\n    display: inline-flex;\n    align-items: center;\n    justify-content: center;\n    width: 24px;\n    height: 24px;\n    line-height: 1;\n}\n\n.chevron.expanded {\n    transform: rotate(180deg);\n}\n\n.loading {\n    animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n    0% {\n        transform: rotate(0deg);\n    }\n\n    100% {\n        transform: rotate(360deg);\n    }\n}\n\n.locate-button:hover {\n    background-color: #2a4365;\n}\n\n.suggest-button,\n.locate-button {\n    background-color: #2C5B8E;\n    color: white;\n    font-family: Inter, sans-serif;\n    flex: 0 0 auto;\n    min-width: 140px;\n    white-space: normal;\n    word-wrap: break-word;\n}\n\n.apply-alt-button {\n    background-color: #2C5B8E;\n    color: white;\n    font-family: Inter, sans-serif;\n    flex: 0 0 auto;\n    min-width: 90px;\n    white-space: normal;\n    word-wrap: break-word;\n    max-width: 25%;\n}\n\n.suggest-button div,\n.apply-alt-button div,\n.locate-button div {\n    text-align: left;\n    flex: 1;\n}\n\n.suggest-button svg,\n.apply-alt-button svg,\n.locate-button svg {\n    flex-shrink: 0;\n}\n\n.suggest-button {\n    max-width: 60%;\n}\n\n.suggest-button:hover {\n    background-color: #2a4365;\n}\n\n.apply-alt-button:hover {\n    background-color: #2a4365;\n}\n\n/* Material Icons Styles */\n.material-icons {\n    font-family: 'Material Icons';\n    font-weight: normal;\n    font-style: normal;\n    font-size: 24px;\n    /* Preferred icon size */\n    display: inline-block;\n    line-height: 1;\n    text-transform: none;\n    letter-spacing: normal;\n    word-wrap: normal;\n    white-space: nowrap;\n    direction: ltr;\n    vertical-align: middle;\n}\n\n/* Icon sizes */\n.material-icons.md-18 {\n    font-size: 18px;\n}\n\n.material-icons.md-24 {\n    font-size: 24px;\n}\n\n.material-icons.md-36 {\n    font-size: 36px;\n}\n\n.material-icons.md-48 {\n    font-size: 48px;\n}\n\n/* Icon colors */\n.material-icons.md-dark {\n    color: rgba(0, 0, 0, 0.54);\n}\n\n.material-icons.md-dark.md-inactive {\n    color: rgba(0, 0, 0, 0.26);\n}\n\n.material-icons.md-light {\n    color: rgba(255, 255, 255, 1);\n}\n\n.material-icons.md-light.md-inactive {\n    color: rgba(255, 255, 255, 0.3);\n}\n\n/* Loading animation for Material Icons */\n.material-icons.loading {\n    animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n    0% {\n        transform: rotate(0deg);\n    }\n\n    100% {\n        transform: rotate(360deg);\n    }\n}\n\n.hidden:not(.dropdown-content) {\n    display: none;\n}\n\n.table-header-fix-widget {\n    margin-top: 8px;\n}\n\n.table-header-fix-widget .button-container {\n    display: flex;\n    justify-content: flex-end;\n    gap: 8px;\n}\n\n.custom-dropdown {\n    position: relative;\n    width: calc(100% - 16px);\n    margin-bottom: 8px;\n    z-index: 9999;\n    isolation: isolate;\n}\n\n.dropdown-button {\n    width: 100%;\n    padding: 8px 12px;\n    background-color: white;\n    color: black;\n    border: 1px solid black;\n    border-radius: 4px;\n    cursor: pointer;\n    font-family: Inter, sans-serif;\n    font-size: 14px;\n    height: 40px;\n    display: flex;\n    align-items: center;\n    justify-content: space-between;\n}\n\n.dropdown-button:hover {\n    background-color: #2a4365;\n    color: white;\n}\n\n.dropdown-button.active {\n    background-color: #2a4365;\n    color: white;\n}\n\n.dropdown-text {\n    flex: 1;\n    text-align: left;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n}\n\n.dropdown-arrow {\n    margin-left: 8px;\n    flex-shrink: 0;\n}\n\n.dropdown-content {\n    position: absolute;\n    top: 100%;\n    left: 0;\n    right: 0;\n    background-color: white;\n    border: 1px solid black;\n    border-radius: 4px;\n    margin-top: 4px;\n    z-index: 1000;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n}\n\n.dropdown-content.hidden {\n    display: none;\n}\n\n.dropdown-option {\n    padding: 8px 12px;\n    cursor: pointer;\n}\n\n.dropdown-option:hover {\n    background-color: #2a4365;\n    color: white;\n}\n\n.table-header-fix-widget {\n    margin-top: 8px;\n}\n\n.table-header-fix-widget .button-container {\n    display: flex;\n    justify-content: flex-end;\n    gap: 8px;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.e97062042ef85814e466.js.map