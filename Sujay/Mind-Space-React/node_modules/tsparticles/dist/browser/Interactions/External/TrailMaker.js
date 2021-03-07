import { Utils } from "../../Utils";
import { ClickMode, HoverMode } from "../../Enums/Modes";
export class TrailMaker {
    constructor(container) {
        this.container = container;
        this.delay = 0;
    }
    interact(delta) {
        if (!this.container.retina.reduceFactor) {
            return;
        }
        const container = this.container;
        const options = container.options;
        const trailOptions = options.interactivity.modes.trail;
        const optDelay = (trailOptions.delay * 1000) / this.container.retina.reduceFactor;
        if (this.delay < optDelay) {
            this.delay += delta.value;
        }
        if (this.delay >= optDelay) {
            container.particles.push(trailOptions.quantity, container.interactivity.mouse, trailOptions.particles);
            this.delay -= optDelay;
        }
    }
    isEnabled() {
        const container = this.container;
        const options = container.options;
        const mouse = container.interactivity.mouse;
        const events = options.interactivity.events;
        return ((mouse.clicking &&
            mouse.inside &&
            !!mouse.position &&
            Utils.isInArray(ClickMode.trail, events.onClick.mode)) ||
            (mouse.inside && !!mouse.position && Utils.isInArray(HoverMode.trail, events.onHover.mode)));
    }
    reset() {
    }
}
