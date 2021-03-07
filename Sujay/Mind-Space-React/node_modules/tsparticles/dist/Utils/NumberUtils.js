"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NumberUtils = void 0;
const Directions_1 = require("../Enums/Directions");
class NumberUtils {
    static clamp(num, min, max) {
        return Math.min(Math.max(num, min), max);
    }
    static mix(comp1, comp2, weight1, weight2) {
        return Math.floor((comp1 * weight1 + comp2 * weight2) / (weight1 + weight2));
    }
    static randomInRange(r1, r2) {
        const max = Math.max(r1, r2), min = Math.min(r1, r2);
        return Math.random() * (max - min) + min;
    }
    static getValue(options) {
        const random = options.random;
        const { enable, minimumValue } = typeof random === "boolean" ? { enable: random, minimumValue: 0 } : random;
        return enable ? NumberUtils.randomInRange(minimumValue, options.value) : options.value;
    }
    static getDistances(pointA, pointB) {
        const dx = pointA.x - pointB.x;
        const dy = pointA.y - pointB.y;
        return { dx: dx, dy: dy, distance: Math.sqrt(dx * dx + dy * dy) };
    }
    static getDistance(pointA, pointB) {
        return NumberUtils.getDistances(pointA, pointB).distance;
    }
    static getParticleBaseVelocity(particle) {
        let velocityBase;
        switch (particle.direction) {
            case Directions_1.MoveDirection.top:
                velocityBase = { x: 0, y: -1 };
                break;
            case Directions_1.MoveDirection.topRight:
                velocityBase = { x: 0.5, y: -0.5 };
                break;
            case Directions_1.MoveDirection.right:
                velocityBase = { x: 1, y: -0 };
                break;
            case Directions_1.MoveDirection.bottomRight:
                velocityBase = { x: 0.5, y: 0.5 };
                break;
            case Directions_1.MoveDirection.bottom:
                velocityBase = { x: 0, y: 1 };
                break;
            case Directions_1.MoveDirection.bottomLeft:
                velocityBase = { x: -0.5, y: 1 };
                break;
            case Directions_1.MoveDirection.left:
                velocityBase = { x: -1, y: 0 };
                break;
            case Directions_1.MoveDirection.topLeft:
                velocityBase = { x: -0.5, y: -0.5 };
                break;
            default:
                velocityBase = { x: 0, y: 0 };
                break;
        }
        return velocityBase;
    }
    static rotateVelocity(velocity, angle) {
        return {
            horizontal: velocity.horizontal * Math.cos(angle) - velocity.vertical * Math.sin(angle),
            vertical: velocity.horizontal * Math.sin(angle) + velocity.vertical * Math.cos(angle),
        };
    }
    static collisionVelocity(v1, v2, m1, m2) {
        return {
            horizontal: (v1.horizontal * (m1 - m2)) / (m1 + m2) + (v2.horizontal * 2 * m2) / (m1 + m2),
            vertical: v1.vertical,
        };
    }
}
exports.NumberUtils = NumberUtils;
