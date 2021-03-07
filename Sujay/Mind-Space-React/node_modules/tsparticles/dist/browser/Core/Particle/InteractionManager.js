import { Grabber } from "../../Interactions/External/Grabber";
import { Repulser } from "../../Interactions/External/Repulser";
import { Bubbler } from "../../Interactions/External/Bubbler";
import { Connector } from "../../Interactions/External/Connector";
import { Linker } from "../../Interactions/Particles/Linker";
import { Attractor as ParticlesAttractor } from "../../Interactions/Particles/Attractor";
import { Collider } from "../../Interactions/Particles/Collider";
import { Infecter } from "../../Interactions/Particles/Infecter";
import { TrailMaker } from "../../Interactions/External/TrailMaker";
import { Attractor as MouseAttractor } from "../../Interactions/External/Attractor";
import { Lighter as ParticlesLighter } from "../../Interactions/Particles/Lighter";
import { Lighter as MouseLighter } from "../../Interactions/External/Lighter";
import { Bouncer } from "../../Interactions/External/Bouncer";
export class InteractionManager {
    constructor(container) {
        this.container = container;
        this.externalInteractors = [
            new Bouncer(container),
            new Bubbler(container),
            new Connector(container),
            new Grabber(container),
            new MouseLighter(container),
            new MouseAttractor(container),
            new Repulser(container),
            new TrailMaker(container),
        ];
        this.particleInteractors = [
            new ParticlesAttractor(container),
            new ParticlesLighter(container),
            new Collider(container),
            new Infecter(container),
            new Linker(container),
        ];
    }
    init() {
    }
    externalInteract(delta) {
        for (const interactor of this.externalInteractors) {
            if (interactor.isEnabled()) {
                interactor.interact(delta);
            }
        }
    }
    particlesInteract(particle, delta) {
        for (const interactor of this.externalInteractors) {
            interactor.reset(particle);
        }
        for (const interactor of this.particleInteractors) {
            if (interactor.isEnabled(particle)) {
                interactor.interact(particle, delta);
            }
        }
    }
}
