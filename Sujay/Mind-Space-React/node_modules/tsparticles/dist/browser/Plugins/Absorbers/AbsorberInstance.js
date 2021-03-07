import { ColorUtils, NumberUtils, Utils } from "../../Utils";
export class AbsorberInstance {
    constructor(absorbers, container, options, position) {
        var _a, _b;
        this.absorbers = absorbers;
        this.container = container;
        this.initialPosition = position;
        this.options = options;
        this.dragging = false;
        this.opacity = this.options.opacity;
        this.size = NumberUtils.getValue(options.size) * container.retina.pixelRatio;
        this.mass = this.size * options.size.density * container.retina.reduceFactor;
        const limit = options.size.limit;
        this.limit = limit !== undefined ? limit * container.retina.pixelRatio * container.retina.reduceFactor : limit;
        const color = typeof options.color === "string" ? { value: options.color } : options.color;
        this.color = (_a = ColorUtils.colorToRgb(color)) !== null && _a !== void 0 ? _a : {
            b: 0,
            g: 0,
            r: 0,
        };
        this.position = (_b = this.initialPosition) !== null && _b !== void 0 ? _b : this.calcPosition();
    }
    attract(particle) {
        const options = this.options;
        if (options.draggable) {
            const mouse = this.container.interactivity.mouse;
            if (mouse.clicking && mouse.downPosition) {
                const mouseDist = NumberUtils.getDistance(this.position, mouse.downPosition);
                if (mouseDist <= this.size) {
                    this.dragging = true;
                }
            }
            else {
                this.dragging = false;
            }
            if (this.dragging && mouse.position) {
                this.position.x = mouse.position.x;
                this.position.y = mouse.position.y;
            }
        }
        const pos = particle.getPosition();
        const { dx, dy, distance } = NumberUtils.getDistances(this.position, pos);
        const angle = Math.atan2(dx, dy);
        const acceleration = (this.mass / Math.pow(distance, 2)) * this.container.retina.reduceFactor;
        if (distance < this.size + particle.getRadius()) {
            const sizeFactor = particle.getRadius() * 0.033 * this.container.retina.pixelRatio;
            if (this.size > particle.getRadius() && distance < this.size - particle.getRadius()) {
                if (options.destroy) {
                    particle.destroy();
                }
                else {
                    particle.needsNewPosition = true;
                    this.updateParticlePosition(particle, angle, acceleration);
                }
            }
            else {
                if (options.destroy) {
                    particle.size.value -= sizeFactor;
                }
                this.updateParticlePosition(particle, angle, acceleration);
            }
            if (this.limit === undefined || this.size < this.limit) {
                this.size += sizeFactor;
            }
            this.mass += sizeFactor * this.options.size.density * this.container.retina.reduceFactor;
        }
        else {
            this.updateParticlePosition(particle, angle, acceleration);
        }
    }
    resize() {
        const initialPosition = this.initialPosition;
        this.position =
            initialPosition && Utils.isPointInside(initialPosition, this.container.canvas.size)
                ? initialPosition
                : this.calcPosition();
    }
    draw(context) {
        context.translate(this.position.x, this.position.y);
        context.beginPath();
        context.arc(0, 0, this.size, 0, Math.PI * 2, false);
        context.closePath();
        context.fillStyle = ColorUtils.getStyleFromRgb(this.color, this.opacity);
        context.fill();
    }
    calcPosition() {
        var _a, _b;
        const container = this.container;
        const percentPosition = this.options.position;
        return {
            x: (((_a = percentPosition === null || percentPosition === void 0 ? void 0 : percentPosition.x) !== null && _a !== void 0 ? _a : Math.random() * 100) / 100) * container.canvas.size.width,
            y: (((_b = percentPosition === null || percentPosition === void 0 ? void 0 : percentPosition.y) !== null && _b !== void 0 ? _b : Math.random() * 100) / 100) * container.canvas.size.height,
        };
    }
    updateParticlePosition(particle, angle, acceleration) {
        var _a;
        if (particle.destroyed) {
            return;
        }
        const canvasSize = this.container.canvas.size;
        if (particle.needsNewPosition) {
            const pSize = particle.getRadius();
            particle.position.x = Math.random() * (canvasSize.width - pSize * 2) + pSize;
            particle.position.y = Math.random() * (canvasSize.height - pSize * 2) + pSize;
            particle.needsNewPosition = false;
        }
        if (this.options.orbits) {
            if (particle.orbitRadius === undefined) {
                particle.orbitRadius = NumberUtils.getDistance(particle.getPosition(), this.position);
            }
            if (particle.orbitRadius <= this.size && !this.options.destroy) {
                particle.orbitRadius = Math.random() * Math.max(canvasSize.width, canvasSize.height);
            }
            if (particle.orbitAngle === undefined) {
                particle.orbitAngle = Math.random() * Math.PI * 2;
            }
            const orbitRadius = particle.orbitRadius;
            const orbitAngle = particle.orbitAngle;
            particle.velocity.horizontal = 0;
            particle.velocity.vertical = 0;
            particle.position.x = this.position.x + orbitRadius * Math.cos(orbitAngle);
            particle.position.y = this.position.y + orbitRadius * Math.sin(orbitAngle);
            particle.orbitRadius -= acceleration;
            particle.orbitAngle +=
                (((_a = particle.moveSpeed) !== null && _a !== void 0 ? _a : this.container.retina.moveSpeed) / 100) * this.container.retina.reduceFactor;
        }
        else {
            particle.velocity.horizontal += Math.sin(angle) * acceleration;
            particle.velocity.vertical += Math.cos(angle) * acceleration;
        }
    }
}
