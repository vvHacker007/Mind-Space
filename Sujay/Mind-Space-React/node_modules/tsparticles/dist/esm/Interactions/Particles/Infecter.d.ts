import type { Particle } from "../../Core/Particle";
import type { Container } from "../../Core/Container";
import type { IParticlesInteractor } from "../../Core/Interfaces/IParticlesInteractor";
import type { IDelta } from "../../Core/Interfaces/IDelta";
export declare class Infecter implements IParticlesInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(): boolean;
    reset(): void;
    interact(p1: Particle, delta: IDelta): void;
}
