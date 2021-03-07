import type { Container } from "../Container";
import type { Particle } from "../Particle";
import type { IDelta } from "../Interfaces/IDelta";
export declare class Mover {
    private readonly container;
    private readonly particle;
    constructor(container: Container, particle: Particle);
    move(delta: IDelta): void;
    private moveParticle;
    private applyNoise;
    private moveParallax;
    private getProximitySpeedFactor;
}
