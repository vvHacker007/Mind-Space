"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Bouncer = void 0;
const Utils_1 = require("../../Utils");
const Modes_1 = require("../../Enums/Modes");
const Utils_2 = require("../../Utils");
const Modes_2 = require("../../Enums/Modes");
const Types_1 = require("../../Enums/Types");
class Bouncer {
    constructor(container) {
        this.container = container;
    }
    isEnabled() {
        const container = this.container;
        const options = container.options;
        const mouse = container.interactivity.mouse;
        const events = options.interactivity.events;
        const divs = events.onDiv;
        return ((mouse.position && events.onHover.enable && Utils_2.Utils.isInArray(Modes_1.HoverMode.bounce, events.onHover.mode)) ||
            Utils_2.Utils.isDivModeEnabled(Modes_2.DivMode.bounce, divs));
    }
    interact() {
        const container = this.container;
        const options = container.options;
        const events = options.interactivity.events;
        const mouseMoveStatus = container.interactivity.status === Utils_1.Constants.mouseMoveEvent;
        const hoverEnabled = events.onHover.enable;
        const hoverMode = events.onHover.mode;
        const divs = events.onDiv;
        if (mouseMoveStatus && hoverEnabled && Utils_2.Utils.isInArray(Modes_1.HoverMode.bounce, hoverMode)) {
            this.processMouseBounce();
        }
        else {
            Utils_2.Utils.divModeExecute(Modes_2.DivMode.bounce, divs, (selector, div) => this.singleSelectorBounce(selector, div));
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
            this.processBounce(mousePos, radius, new Utils_2.Circle(mousePos.x, mousePos.y, radius + tolerance));
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
            const area = div.type === Types_1.DivType.circle
                ? new Utils_2.Circle(pos.x, pos.y, radius + tolerance)
                : new Utils_2.Rectangle(elem.offsetLeft * pxRatio - tolerance, elem.offsetTop * pxRatio - tolerance, elem.offsetWidth * pxRatio + tolerance * 2, elem.offsetHeight * pxRatio + tolerance * 2);
            this.processBounce(pos, radius, area);
        });
    }
    processBounce(position, radius, area) {
        const query = this.container.particles.quadTree.query(area);
        for (const particle of query) {
            if (area instanceof Utils_2.Circle) {
                Utils_2.Utils.circleBounce(Utils_2.Utils.circleBounceDataFromParticle(particle), {
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
            else if (area instanceof Utils_2.Rectangle) {
                Utils_2.Utils.rectBounce(particle, Utils_2.Utils.calculateBounds(position, radius));
            }
        }
    }
}
exports.Bouncer = Bouncer;
