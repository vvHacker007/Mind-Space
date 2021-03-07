import { Utils } from "../../Utils";
import { HoverMode } from "../../Enums/Modes";
export class Lighter {
    constructor(container) {
        this.container = container;
    }
    interact(particle) {
        const container = this.container;
        const options = container.options;
        if (options.interactivity.events.onHover.enable && container.interactivity.status === "mousemove") {
            const mousePos = this.container.interactivity.mouse.position;
            if (mousePos) {
                container.canvas.drawParticleShadow(particle, mousePos);
            }
        }
    }
    isEnabled() {
        const container = this.container;
        const mouse = container.interactivity.mouse;
        const events = container.options.interactivity.events;
        if (!(events.onHover.enable && mouse.position)) {
            return false;
        }
        const hoverMode = events.onHover.mode;
        return Utils.isInArray(HoverMode.light, hoverMode);
    }
    reset() {
    }
}
