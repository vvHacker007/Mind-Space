import type { IParticle } from "../../Core/Interfaces/IParticle";
import type { Container } from "../../Core/Container";
import { Particle } from "../../Core/Particle";
import type { IParticlesInteractor } from "../../Core/Interfaces/IParticlesInteractor";
export declare class Attractor implements IParticlesInteractor {
    private readonly container;
    constructor(container: Container);
    interact(p1: IParticle): void;
    isEnabled(particle: Particle): boolean;
    reset(): void;
}
