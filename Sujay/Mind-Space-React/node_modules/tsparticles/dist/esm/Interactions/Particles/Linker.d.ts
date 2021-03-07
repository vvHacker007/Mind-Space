import { Particle } from "../../Core/Particle";
import type { Container } from "../../Core/Container";
import { IParticlesInteractor } from "../../Core/Interfaces/IParticlesInteractor";
import { IParticle } from "../../Core/Interfaces/IParticle";
export declare class Linker implements IParticlesInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(particle: Particle): boolean;
    reset(): void;
    interact(p1: IParticle): void;
}
