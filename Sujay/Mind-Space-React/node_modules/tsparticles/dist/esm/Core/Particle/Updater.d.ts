import type { Container } from "../Container";
import type { Particle } from "../Particle";
import type { IDelta } from "../Interfaces/IDelta";
export declare class Updater {
    private readonly container;
    private readonly particle;
    constructor(container: Container, particle: Particle);
    update(delta: IDelta): void;
    private updateLife;
    private updateOpacity;
    private updateSize;
    private updateAngle;
    private updateColor;
    private updateStrokeColor;
    private updateOutModes;
    private updateOutMode;
    private fixOutOfCanvasPosition;
    private updateBounce;
    private bounceNone;
}
