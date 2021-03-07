"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Updater = void 0;
const Utils_1 = require("../../Utils");
const Enums_1 = require("../../Enums");
const OutModeDirection_1 = require("../../Enums/Directions/OutModeDirection");
function bounceHorizontal(data) {
    if (data.outMode === Enums_1.OutMode.bounce ||
        data.outMode === Enums_1.OutMode.bounceHorizontal ||
        data.outMode === "bounceHorizontal") {
        const velocity = data.particle.velocity.horizontal;
        let bounced = false;
        if ((data.direction === OutModeDirection_1.OutModeDirection.right && data.bounds.right >= data.canvasSize.width && velocity > 0) ||
            (data.direction === OutModeDirection_1.OutModeDirection.left && data.bounds.left <= 0 && velocity < 0)) {
            const newVelocity = Utils_1.NumberUtils.getValue(data.particle.particlesOptions.bounce.horizontal);
            data.particle.velocity.horizontal *= -newVelocity;
            bounced = true;
        }
        if (bounced) {
            const minPos = data.offset.x + data.size;
            if (data.bounds.right >= data.canvasSize.width) {
                data.particle.position.x = data.canvasSize.width - minPos;
            }
            else if (data.bounds.left <= 0) {
                data.particle.position.x = minPos;
            }
        }
    }
}
function bounceVertical(data) {
    if (data.outMode === Enums_1.OutMode.bounce ||
        data.outMode === Enums_1.OutMode.bounceVertical ||
        data.outMode === "bounceVertical") {
        const velocity = data.particle.velocity.vertical;
        let bounced = false;
        if ((data.direction === OutModeDirection_1.OutModeDirection.bottom &&
            data.bounds.bottom >= data.canvasSize.height &&
            velocity > 0) ||
            (data.direction === OutModeDirection_1.OutModeDirection.top && data.bounds.top <= 0 && velocity < 0)) {
            const newVelocity = Utils_1.NumberUtils.getValue(data.particle.particlesOptions.bounce.vertical);
            data.particle.velocity.vertical *= -newVelocity;
            bounced = true;
        }
        if (bounced) {
            const minPos = data.offset.y + data.size;
            if (data.bounds.bottom >= data.canvasSize.height) {
                data.particle.position.y = data.canvasSize.height - minPos;
            }
            else if (data.bounds.top <= 0) {
                data.particle.position.y = minPos;
            }
        }
    }
}
function checkDestroy(particle, destroy, value, minValue, maxValue) {
    switch (destroy) {
        case Enums_1.DestroyType.max:
            if (value >= maxValue) {
                particle.destroy();
            }
            break;
        case Enums_1.DestroyType.min:
            if (value <= minValue) {
                particle.destroy();
            }
            break;
    }
}
class Updater {
    constructor(container, particle) {
        this.container = container;
        this.particle = particle;
    }
    update(delta) {
        if (this.particle.destroyed) {
            return;
        }
        this.updateLife(delta);
        if (this.particle.destroyed || this.particle.spawning) {
            return;
        }
        this.updateOpacity(delta);
        this.updateSize(delta);
        this.updateAngle(delta);
        this.updateColor(delta);
        this.updateStrokeColor(delta);
        this.updateOutModes(delta);
    }
    updateLife(delta) {
        const particle = this.particle;
        let justSpawned = false;
        if (particle.spawning) {
            particle.lifeDelayTime += delta.value;
            if (particle.lifeDelayTime >= particle.lifeDelay) {
                justSpawned = true;
                particle.spawning = false;
                particle.lifeDelayTime = 0;
                particle.lifeTime = 0;
            }
        }
        if (particle.lifeDuration === -1) {
            return;
        }
        if (!particle.spawning) {
            if (justSpawned) {
                particle.lifeTime = 0;
            }
            else {
                particle.lifeTime += delta.value;
            }
            if (particle.lifeTime >= particle.lifeDuration) {
                particle.lifeTime = 0;
                if (particle.livesRemaining > 0) {
                    particle.livesRemaining--;
                }
                if (particle.livesRemaining === 0) {
                    particle.destroy();
                    return;
                }
                const canvasSize = this.container.canvas.size;
                particle.position.x = Utils_1.NumberUtils.randomInRange(0, canvasSize.width);
                particle.position.y = Utils_1.NumberUtils.randomInRange(0, canvasSize.height);
                particle.spawning = true;
                particle.lifeDelayTime = 0;
                particle.lifeTime = 0;
                const lifeOptions = particle.particlesOptions.life;
                particle.lifeDelay = Utils_1.NumberUtils.getValue(lifeOptions.delay) * 1000;
                particle.lifeDuration = Utils_1.NumberUtils.getValue(lifeOptions.duration) * 1000;
            }
        }
    }
    updateOpacity(delta) {
        var _a, _b;
        const particle = this.particle;
        const opacityAnim = particle.particlesOptions.opacity.anim;
        const minValue = opacityAnim.minimumValue;
        const maxValue = particle.particlesOptions.opacity.value;
        if (opacityAnim.enable) {
            switch (particle.opacity.status) {
                case Enums_1.AnimationStatus.increasing:
                    if (particle.opacity.value >= maxValue) {
                        particle.opacity.status = Enums_1.AnimationStatus.decreasing;
                    }
                    else {
                        particle.opacity.value += ((_a = particle.opacity.velocity) !== null && _a !== void 0 ? _a : 0) * delta.factor;
                    }
                    break;
                case Enums_1.AnimationStatus.decreasing:
                    if (particle.opacity.value <= minValue) {
                        particle.opacity.status = Enums_1.AnimationStatus.increasing;
                    }
                    else {
                        particle.opacity.value -= ((_b = particle.opacity.velocity) !== null && _b !== void 0 ? _b : 0) * delta.factor;
                    }
                    break;
            }
            checkDestroy(particle, opacityAnim.destroy, particle.opacity.value, minValue, maxValue);
            if (!particle.destroyed) {
                particle.opacity.value = Utils_1.NumberUtils.clamp(particle.opacity.value, minValue, maxValue);
            }
        }
    }
    updateSize(delta) {
        var _a, _b;
        const container = this.container;
        const particle = this.particle;
        const sizeOpt = particle.particlesOptions.size;
        const sizeAnim = sizeOpt.animation;
        const sizeVelocity = ((_a = particle.size.velocity) !== null && _a !== void 0 ? _a : 0) * delta.factor;
        const maxValue = (_b = particle.sizeValue) !== null && _b !== void 0 ? _b : container.retina.sizeValue;
        const minValue = sizeAnim.minimumValue * container.retina.pixelRatio;
        if (sizeAnim.enable) {
            switch (particle.size.status) {
                case Enums_1.AnimationStatus.increasing:
                    if (particle.size.value >= maxValue) {
                        particle.size.status = Enums_1.AnimationStatus.decreasing;
                    }
                    else {
                        particle.size.value += sizeVelocity;
                    }
                    break;
                case Enums_1.AnimationStatus.decreasing:
                    if (particle.size.value <= minValue) {
                        particle.size.status = Enums_1.AnimationStatus.increasing;
                    }
                    else {
                        particle.size.value -= sizeVelocity;
                    }
            }
            checkDestroy(particle, sizeAnim.destroy, particle.size.value, minValue, maxValue);
            if (!particle.destroyed) {
                particle.size.value = Utils_1.NumberUtils.clamp(particle.size.value, minValue, maxValue);
            }
        }
    }
    updateAngle(delta) {
        var _a;
        const particle = this.particle;
        const rotate = particle.particlesOptions.rotate;
        const rotateAnimation = rotate.animation;
        const speed = ((_a = particle.rotate.velocity) !== null && _a !== void 0 ? _a : 0) * delta.factor;
        const max = 2 * Math.PI;
        if (rotate.path) {
            particle.pathAngle = Math.atan2(particle.velocity.vertical, particle.velocity.horizontal);
        }
        else if (rotateAnimation.enable) {
            switch (particle.rotate.status) {
                case Enums_1.AnimationStatus.increasing:
                    particle.rotate.value += speed;
                    if (particle.rotate.value > max) {
                        particle.rotate.value -= max;
                    }
                    break;
                case Enums_1.AnimationStatus.decreasing:
                default:
                    particle.rotate.value -= speed;
                    if (particle.rotate.value < 0) {
                        particle.rotate.value += max;
                    }
                    break;
            }
        }
    }
    updateColor(delta) {
        var _a;
        const particle = this.particle;
        if (particle.color.value === undefined) {
            return;
        }
        if (particle.particlesOptions.color.animation.enable) {
            particle.color.value.h += ((_a = particle.color.velocity) !== null && _a !== void 0 ? _a : 0) * delta.factor;
            if (particle.color.value.h > 360) {
                particle.color.value.h -= 360;
            }
        }
    }
    updateStrokeColor(delta) {
        var _a, _b;
        const particle = this.particle;
        const color = particle.stroke.color;
        if (typeof color === "string" || color === undefined) {
            return;
        }
        if (particle.strokeColor.value === undefined) {
            return;
        }
        if (color.animation.enable) {
            particle.strokeColor.value.h +=
                ((_b = (_a = particle.strokeColor.velocity) !== null && _a !== void 0 ? _a : particle.color.velocity) !== null && _b !== void 0 ? _b : 0) * delta.factor;
            if (particle.strokeColor.value.h > 360) {
                particle.strokeColor.value.h -= 360;
            }
        }
    }
    updateOutModes(delta) {
        var _a, _b, _c, _d;
        const outModes = this.particle.particlesOptions.move.outModes;
        this.updateOutMode(delta, (_a = outModes.bottom) !== null && _a !== void 0 ? _a : outModes.default, OutModeDirection_1.OutModeDirection.bottom);
        this.updateOutMode(delta, (_b = outModes.left) !== null && _b !== void 0 ? _b : outModes.default, OutModeDirection_1.OutModeDirection.left);
        this.updateOutMode(delta, (_c = outModes.right) !== null && _c !== void 0 ? _c : outModes.default, OutModeDirection_1.OutModeDirection.right);
        this.updateOutMode(delta, (_d = outModes.top) !== null && _d !== void 0 ? _d : outModes.default, OutModeDirection_1.OutModeDirection.top);
    }
    updateOutMode(delta, outMode, direction) {
        const container = this.container;
        const particle = this.particle;
        switch (outMode) {
            case Enums_1.OutMode.bounce:
            case Enums_1.OutMode.bounceVertical:
            case Enums_1.OutMode.bounceHorizontal:
            case "bounceVertical":
            case "bounceHorizontal":
                this.updateBounce(delta, direction, outMode);
                break;
            case Enums_1.OutMode.destroy:
                if (!Utils_1.Utils.isPointInside(particle.position, container.canvas.size, particle.getRadius(), direction)) {
                    container.particles.remove(particle);
                }
                break;
            case Enums_1.OutMode.out:
                if (!Utils_1.Utils.isPointInside(particle.position, container.canvas.size, particle.getRadius(), direction)) {
                    this.fixOutOfCanvasPosition(direction);
                }
                break;
            case Enums_1.OutMode.none:
                this.bounceNone(direction);
                break;
        }
    }
    fixOutOfCanvasPosition(direction) {
        const container = this.container;
        const particle = this.particle;
        const wrap = particle.particlesOptions.move.warp;
        const canvasSize = container.canvas.size;
        const newPos = {
            bottom: canvasSize.height + particle.getRadius() - particle.offset.y,
            left: -particle.getRadius() - particle.offset.x,
            right: canvasSize.width + particle.getRadius() + particle.offset.x,
            top: -particle.getRadius() - particle.offset.y,
        };
        const sizeValue = particle.getRadius();
        const nextBounds = Utils_1.Utils.calculateBounds(particle.position, sizeValue);
        if (direction === OutModeDirection_1.OutModeDirection.right && nextBounds.left > canvasSize.width - particle.offset.x) {
            particle.position.x = newPos.left;
            if (!wrap) {
                particle.position.y = Math.random() * canvasSize.height;
            }
        }
        else if (direction === OutModeDirection_1.OutModeDirection.left && nextBounds.right < -particle.offset.x) {
            particle.position.x = newPos.right;
            if (!wrap) {
                particle.position.y = Math.random() * canvasSize.height;
            }
        }
        if (direction === OutModeDirection_1.OutModeDirection.bottom && nextBounds.top > canvasSize.height - particle.offset.y) {
            if (!wrap) {
                particle.position.x = Math.random() * canvasSize.width;
            }
            particle.position.y = newPos.top;
        }
        else if (direction === OutModeDirection_1.OutModeDirection.top && nextBounds.bottom < -particle.offset.y) {
            if (!wrap) {
                particle.position.x = Math.random() * canvasSize.width;
            }
            particle.position.y = newPos.bottom;
        }
    }
    updateBounce(delta, direction, outMode) {
        const container = this.container;
        const particle = this.particle;
        let handled = false;
        for (const [, plugin] of container.plugins) {
            if (plugin.particleBounce !== undefined) {
                handled = plugin.particleBounce(particle, delta, direction);
            }
            if (handled) {
                break;
            }
        }
        if (handled) {
            return;
        }
        const pos = particle.getPosition(), offset = particle.offset, size = particle.getRadius(), bounds = Utils_1.Utils.calculateBounds(pos, size), canvasSize = container.canvas.size;
        bounceHorizontal({ particle, outMode, direction, bounds, canvasSize, offset, size });
        bounceVertical({ particle, outMode, direction, bounds, canvasSize, offset, size });
    }
    bounceNone(direction) {
        const particle = this.particle;
        if (particle.particlesOptions.move.distance) {
            return;
        }
        const gravityOptions = particle.particlesOptions.move.gravity;
        const container = this.container;
        if (!gravityOptions.enable) {
            if (!Utils_1.Utils.isPointInside(particle.position, container.canvas.size, particle.getRadius(), direction)) {
                container.particles.remove(particle);
            }
        }
        else {
            const position = particle.position;
            if ((gravityOptions.acceleration >= 0 &&
                position.y > container.canvas.size.height &&
                direction === OutModeDirection_1.OutModeDirection.bottom) ||
                (gravityOptions.acceleration < 0 && position.y < 0 && direction === OutModeDirection_1.OutModeDirection.top)) {
                container.particles.remove(particle);
            }
        }
    }
}
exports.Updater = Updater;
