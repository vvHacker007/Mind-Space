"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Main = void 0;
const main_slim_1 = require("./main.slim");
const AbsorbersPlugin_1 = require("./Plugins/Absorbers/AbsorbersPlugin");
const EmittersPlugin_1 = require("./Plugins/Emitters/EmittersPlugin");
const PolygonMaskPlugin_1 = require("./Plugins/PolygonMask/PolygonMaskPlugin");
class Main extends main_slim_1.MainSlim {
    constructor() {
        super();
        this.addPlugin(AbsorbersPlugin_1.AbsorbersPlugin);
        this.addPlugin(EmittersPlugin_1.EmittersPlugin);
        this.addPlugin(PolygonMaskPlugin_1.PolygonMaskPlugin);
    }
}
exports.Main = Main;
