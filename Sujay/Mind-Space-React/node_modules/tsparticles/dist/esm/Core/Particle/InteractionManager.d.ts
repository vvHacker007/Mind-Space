import type { Container } from "../Container";
import type { IDelta } from "../Interfaces/IDelta";
import { Particle } from "../Particle";
export declare class InteractionManager {
    private readonly container;
    private readonly externalInteractors;
    private readonly particleInteractors;
    constructor(container: Container);
    init(): void;
    externalInteract(delta: IDelta): void;
    particlesInteract(particle: Particle, delta: IDelta): void;
}
