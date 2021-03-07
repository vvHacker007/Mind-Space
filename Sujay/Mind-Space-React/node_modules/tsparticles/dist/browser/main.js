import { MainSlim } from "./main.slim";
import { AbsorbersPlugin } from "./Plugins/Absorbers/AbsorbersPlugin";
import { EmittersPlugin } from "./Plugins/Emitters/EmittersPlugin";
import { PolygonMaskPlugin } from "./Plugins/PolygonMask/PolygonMaskPlugin";
export class Main extends MainSlim {
    constructor() {
        super();
        this.addPlugin(AbsorbersPlugin);
        this.addPlugin(EmittersPlugin);
        this.addPlugin(PolygonMaskPlugin);
    }
}
