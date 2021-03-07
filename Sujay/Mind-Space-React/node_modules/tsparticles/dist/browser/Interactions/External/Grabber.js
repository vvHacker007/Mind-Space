import { Constants, Utils, ColorUtils, NumberUtils } from "../../Utils";
import { HoverMode } from "../../Enums/Modes";
export class Grabber {
    constructor(container) {
        this.container = container;
    }
    isEnabled() {
        const container = this.container;
        const mouse = container.interactivity.mouse;
        const events = container.options.interactivity.events;
        if (!(events.onHover.enable && mouse.position)) {
            return false;
        }
        const hoverMode = events.onHover.mode;
        return Utils.isInArray(HoverMode.grab, hoverMode);
    }
    reset() {
    }
    interact() {
        var _a;
        const container = this.container;
        const options = container.options;
        const interactivity = options.interactivity;
        if (interactivity.events.onHover.enable && container.interactivity.status === Constants.mouseMoveEvent) {
            const mousePos = container.interactivity.mouse.position;
            if (mousePos === undefined) {
                return;
            }
            const distance = container.retina.grabModeDistance;
            const query = container.particles.quadTree.queryCircle(mousePos, distance);
            for (const particle of query) {
                const pos = particle.getPosition();
                const pointDistance = NumberUtils.getDistance(pos, mousePos);
                if (pointDistance <= distance) {
                    const grabLineOptions = interactivity.modes.grab.links;
                    const lineOpacity = grabLineOptions.opacity;
                    const opacityLine = lineOpacity - (pointDistance * lineOpacity) / distance;
                    if (opacityLine > 0) {
                        const optColor = (_a = grabLineOptions.color) !== null && _a !== void 0 ? _a : particle.particlesOptions.links.color;
                        if (!container.particles.grabLineColor) {
                            const linksOptions = container.options.interactivity.modes.grab.links;
                            container.particles.grabLineColor = ColorUtils.getLinkRandomColor(optColor, linksOptions.blink, linksOptions.consent);
                        }
                        const colorLine = ColorUtils.getLinkColor(particle, undefined, container.particles.grabLineColor);
                        if (colorLine === undefined) {
                            return;
                        }
                        container.canvas.drawGrabLine(particle, colorLine, opacityLine, mousePos);
                    }
                }
            }
        }
    }
}
