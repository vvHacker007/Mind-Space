import { MoveDirection } from "../../../../Enums";
import { EmitterRate } from "./EmitterRate";
import { EmitterLife } from "./EmitterLife";
import { Utils } from "../../../../Utils";
import { EmitterSize } from "./EmitterSize";
export class Emitter {
    constructor() {
        this.direction = MoveDirection.none;
        this.life = new EmitterLife();
        this.rate = new EmitterRate();
    }
    load(data) {
        if (data === undefined) {
            return;
        }
        if (data.size !== undefined) {
            if (this.size === undefined) {
                this.size = new EmitterSize();
            }
            this.size.load(data.size);
        }
        if (data.direction !== undefined) {
            this.direction = data.direction;
        }
        this.life.load(data.life);
        if (data.particles !== undefined) {
            this.particles = Utils.deepExtend({}, data.particles);
        }
        this.rate.load(data.rate);
        if (data.position !== undefined) {
            this.position = {
                x: data.position.x,
                y: data.position.y,
            };
        }
    }
}
