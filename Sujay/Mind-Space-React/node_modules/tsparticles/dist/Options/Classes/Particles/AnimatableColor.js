"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnimatableColor = void 0;
const OptionsColor_1 = require("../OptionsColor");
const ColorAnimation_1 = require("./ColorAnimation");
class AnimatableColor extends OptionsColor_1.OptionsColor {
    constructor() {
        super();
        this.animation = new ColorAnimation_1.ColorAnimation();
    }
    static create(source, data) {
        const color = source !== null && source !== void 0 ? source : new AnimatableColor();
        if (data !== undefined) {
            color.load(typeof data === "string" ? { value: data } : data);
        }
        return color;
    }
    load(data) {
        super.load(data);
        this.animation.load(data === null || data === void 0 ? void 0 : data.animation);
    }
}
exports.AnimatableColor = AnimatableColor;
