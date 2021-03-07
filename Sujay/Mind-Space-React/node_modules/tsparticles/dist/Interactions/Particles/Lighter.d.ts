import type { Container } from "../../Core/Container";
import type { IParticlesInteractor } from "../../Core/Interfaces/IParticlesInteractor";
import { Particle } from "../../Core/Particle";
export declare class Lighter implements IParticlesInteractor {
    private readonly container;
    constructor(container: Container);
    interact(particle: Particle): void;
    isEnabled(): boolean;
    reset(): void;
}
