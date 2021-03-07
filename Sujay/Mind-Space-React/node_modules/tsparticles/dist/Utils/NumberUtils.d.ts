import type { IValueWithRandom } from "../Options/Interfaces/IValueWithRandom";
import type { ICoordinates } from "../Core/Interfaces/ICoordinates";
import type { IParticle } from "../Core/Interfaces/IParticle";
import type { IVelocity } from "../Core/Interfaces/IVelocity";
export declare class NumberUtils {
    static clamp(num: number, min: number, max: number): number;
    static mix(comp1: number, comp2: number, weight1: number, weight2: number): number;
    static randomInRange(r1: number, r2: number): number;
    static getValue(options: IValueWithRandom): number;
    static getDistances(pointA: ICoordinates, pointB: ICoordinates): {
        dx: number;
        dy: number;
        distance: number;
    };
    static getDistance(pointA: ICoordinates, pointB: ICoordinates): number;
    static getParticleBaseVelocity(particle: IParticle): ICoordinates;
    static rotateVelocity(velocity: IVelocity, angle: number): IVelocity;
    static collisionVelocity(v1: IVelocity, v2: IVelocity, m1: number, m2: number): IVelocity;
}
