import type { Particle } from "../../Core/Particle";
import type { Container } from "../../Core/Container";
import type { IParticlesInteractor } from "../../Core/Interfaces/IParticlesInteractor";
export declare class Collider implements IParticlesInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(particle: Particle): boolean;
    reset(): void;
    interact(p1: Particle): void;
    private resolveCollision;
    private absorb;
}
