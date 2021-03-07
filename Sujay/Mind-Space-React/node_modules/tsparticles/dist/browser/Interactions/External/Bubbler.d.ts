import type { Container } from "../../Core/Container";
import { Particle } from "../../Core/Particle";
import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
export declare class Bubbler implements IExternalInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(): boolean;
    reset(particle: Particle, force?: boolean): void;
    interact(): void;
    private singleSelectorHover;
    private process;
    private clickBubble;
    private hoverBubble;
    private hoverBubbleSize;
    private hoverBubbleOpacity;
    private hoverBubbleColor;
}
