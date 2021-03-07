import { CollisionMode } from "../../../Enums";
import { Bounce } from "./Bounce/Bounce";
export class Collisions {
    constructor() {
        this.bounce = new Bounce();
        this.enable = false;
        this.mode = CollisionMode.bounce;
    }
    load(data) {
        if (data === undefined) {
            return;
        }
        this.bounce.load(data.bounce);
        if (data.enable !== undefined) {
            this.enable = data.enable;
        }
        if (data.mode !== undefined) {
            this.mode = data.mode;
        }
    }
}
