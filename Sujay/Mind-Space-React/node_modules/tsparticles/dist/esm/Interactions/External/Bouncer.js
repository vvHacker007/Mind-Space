import { Constants } from "../../Utils";
import { HoverMode } from "../../Enums/Modes";
import { Circle, Rectangle, Utils } from "../../Utils";
import { DivMode } from "../../Enums/Modes";
import { DivType } from "../../Enums/Types";
export class Bouncer {
    constructor(container) {
        this.container = container;
    }
    isEnabled() {
        const container = this.container;
        const options = container.options;
        const mouse = container.interactivity.mouse;
        const events = options.interactivity.events;
        const divs = events.onDiv;
        return ((mouse.position && events.onHover.enable && Utils.isInArray(HoverMode.bounce, events.onHover.mode)) ||
            Utils.isDivModeEnabled(DivMode.bounce, divs));
    }
    interact() {
        const container = this.container;
        const options = container.options;
        const events = options.interactivity.events;
        const mouseMoveStatus = container.interactivity.status === Constants.mouseMoveEvent;
        const hoverEnabled = events.onHover.enable;
        const hoverMode = events.onHover.mode;
        const divs = events.onDiv;
        if (mouseMoveStatus && hoverEnabled && Utils.isInArray(HoverMode.bounce, hoverMode)) {
            this.processMouseBounce();
        }
        else {
            Utils.divModeExecute(DivMode.bounce, divs, (selector, div) => this.singleSelectorBounce(selector, div));
        }
    }
    reset() {
    }
    processMouseBounce() {
        const container = this.container;
        const pxRatio = container.retina.pixelRatio;
        const tolerance = 10 * pxRatio;
        const mousePos = container.interactivity.mouse.position;
        const radius = container.retina.bounceModeDistance;
        if (mousePos) {
            this.processBounce(mousePos, radius, new Circle(mousePos.x, mousePos.y, radius + tolerance));
        }
    }
    singleSelectorBounce(selector, div) {
        const container = this.container;
        const query = document.querySelectorAll(selector);
        if (!query.length) {
            return;
        }
        query.forEach((item) => {
            const elem = item;
            const pxRatio = container.retina.pixelRatio;
            const pos = {
                x: (elem.offsetLeft + elem.offsetWidth / 2) * pxRatio,
                y: (elem.offsetTop + elem.offsetHeight / 2) * pxRatio,
            };
            const radius = (elem.offsetWidth / 2) * pxRatio;
            const tolerance = 10 * pxRatio;
            const area = div.type === DivType.circle
                ? new Circle(pos.x, pos.y, radius + tolerance)
                : new Rectangle(elem.offsetLeft * pxRatio - tolerance, elem.offsetTop * pxRatio - tolerance, elem.offsetWidth * pxRatio + tolerance * 2, elem.offsetHeight * pxRatio + tolerance * 2);
            this.processBounce(pos, radius, area);
        });
    }
    processBounce(position, radius, area) {
        const query = this.container.particles.quadTree.query(area);
        for (const particle of query) {
            if (area instanceof Circle) {
                Utils.circleBounce(Utils.circleBounceDataFromParticle(particle), {
                    position,
                    radius,
                    velocity: {
                        horizontal: 0,
                        vertical: 0,
                    },
                    factor: {
                        horizontal: 0,
                        vertical: 0,
                    },
                });
            }
            else if (area instanceof Rectangle) {
                Utils.rectBounce(particle, Utils.calculateBounds(position, radius));
            }
        }
    }
}
