"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Loader = void 0;
const Container_1 = require("./Container");
const Utils_1 = require("../Utils");
const tsParticlesDom = [];
function fetchError(statusCode) {
    console.error(`Error tsParticles - fetch status: ${statusCode}`);
    console.error("Error tsParticles - File config not found");
}
class Loader {
    static dom() {
        return tsParticlesDom;
    }
    static domItem(index) {
        const dom = Loader.dom();
        const item = dom[index];
        if (item && !item.destroyed) {
            return item;
        }
        dom.splice(index, 1);
    }
    static load(tagId, options, index) {
        return __awaiter(this, void 0, void 0, function* () {
            const domContainer = document.getElementById(tagId);
            if (!domContainer) {
                return;
            }
            return Loader.set(tagId, domContainer, options, index);
        });
    }
    static set(id, domContainer, options, index) {
        return __awaiter(this, void 0, void 0, function* () {
            const currentOptions = options instanceof Array ? Utils_1.Utils.itemFromArray(options, index) : options;
            const dom = Loader.dom();
            const oldIndex = dom.findIndex((v) => v.id === id);
            if (oldIndex >= 0) {
                const old = Loader.domItem(oldIndex);
                if (old && !old.destroyed) {
                    old.destroy();
                    dom.splice(oldIndex, 1);
                }
            }
            let canvasEl;
            let generatedCanvas;
            if (domContainer.tagName.toLowerCase() === "canvas") {
                canvasEl = domContainer;
                generatedCanvas = false;
            }
            else {
                const existingCanvases = domContainer.getElementsByTagName("canvas");
                if (existingCanvases.length) {
                    canvasEl = existingCanvases[0];
                    if (!canvasEl.className) {
                        canvasEl.className = Utils_1.Constants.canvasClass;
                    }
                    generatedCanvas = false;
                }
                else {
                    generatedCanvas = true;
                    canvasEl = document.createElement("canvas");
                    canvasEl.className = Utils_1.Constants.canvasClass;
                    canvasEl.style.width = "100%";
                    canvasEl.style.height = "100%";
                    domContainer.appendChild(canvasEl);
                }
            }
            const newItem = new Container_1.Container(id, currentOptions);
            if (oldIndex >= 0) {
                dom.splice(oldIndex, 0, newItem);
            }
            else {
                dom.push(newItem);
            }
            newItem.canvas.loadCanvas(canvasEl, generatedCanvas);
            yield newItem.start();
            return newItem;
        });
    }
    static loadJSON(tagId, jsonUrl, index) {
        return __awaiter(this, void 0, void 0, function* () {
            const url = jsonUrl instanceof Array ? Utils_1.Utils.itemFromArray(jsonUrl, index) : jsonUrl;
            const response = yield fetch(url);
            if (response.ok) {
                return Loader.load(tagId, yield response.json());
            }
            else {
                fetchError(response.status);
            }
        });
    }
    static setJSON(id, domContainer, jsonUrl) {
        return __awaiter(this, void 0, void 0, function* () {
            const response = yield fetch(jsonUrl);
            if (response.ok) {
                const options = yield response.json();
                return Loader.set(id, domContainer, options);
            }
            else {
                fetchError(response.status);
            }
        });
    }
    static setOnClickHandler(callback) {
        const dom = Loader.dom();
        if (dom.length === 0) {
            throw new Error("Can only set click handlers after calling tsParticles.load() or tsParticles.loadJSON()");
        }
        for (const domItem of dom) {
            const el = domItem.interactivity.element;
            if (!el) {
                continue;
            }
            const clickOrTouchHandler = (e, pos) => {
                if (domItem.destroyed) {
                    return;
                }
                const pxRatio = domItem.retina.pixelRatio;
                const posRetina = {
                    x: pos.x * pxRatio,
                    y: pos.y * pxRatio,
                };
                const particles = domItem.particles.quadTree.queryCircle(posRetina, domItem.retina.sizeValue);
                callback(e, particles);
            };
            const clickHandler = (e) => {
                if (domItem.destroyed) {
                    return;
                }
                const mouseEvent = e;
                const pos = {
                    x: mouseEvent.offsetX || mouseEvent.clientX,
                    y: mouseEvent.offsetY || mouseEvent.clientY,
                };
                clickOrTouchHandler(e, pos);
            };
            const touchStartHandler = () => {
                if (domItem.destroyed) {
                    return;
                }
                touched = true;
                touchMoved = false;
            };
            const touchMoveHandler = () => {
                if (domItem.destroyed) {
                    return;
                }
                touchMoved = true;
            };
            const touchEndHandler = (e) => {
                var _a, _b, _c;
                if (domItem.destroyed) {
                    return;
                }
                if (touched && !touchMoved) {
                    const touchEvent = e;
                    const lastTouch = touchEvent.touches[touchEvent.touches.length - 1];
                    const canvasRect = (_a = domItem.canvas.element) === null || _a === void 0 ? void 0 : _a.getBoundingClientRect();
                    const pos = {
                        x: lastTouch.clientX - ((_b = canvasRect === null || canvasRect === void 0 ? void 0 : canvasRect.left) !== null && _b !== void 0 ? _b : 0),
                        y: lastTouch.clientY - ((_c = canvasRect === null || canvasRect === void 0 ? void 0 : canvasRect.top) !== null && _c !== void 0 ? _c : 0),
                    };
                    clickOrTouchHandler(e, pos);
                }
                touched = false;
                touchMoved = false;
            };
            const touchCancelHandler = () => {
                if (domItem.destroyed) {
                    return;
                }
                touched = false;
                touchMoved = false;
            };
            let touched = false;
            let touchMoved = false;
            el.addEventListener("click", clickHandler);
            el.addEventListener("touchstart", touchStartHandler);
            el.addEventListener("touchmove", touchMoveHandler);
            el.addEventListener("touchend", touchEndHandler);
            el.addEventListener("touchcancel", touchCancelHandler);
        }
    }
}
exports.Loader = Loader;
