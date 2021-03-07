import type { Container } from "../../Core/Container";
import type { ICoordinates } from "../../Core/Interfaces/ICoordinates";
import type { IEmitter } from "./Options/Interfaces/IEmitter";
import type { Emitters } from "./Emitters";
import type { IEmitterSize } from "./Options/Interfaces/IEmitterSize";
export declare class EmitterInstance {
    private readonly emitters;
    private readonly container;
    position: ICoordinates;
    size: IEmitterSize;
    emitterOptions: IEmitter;
    private lifeCount;
    private startInterval?;
    private readonly immortal;
    private readonly initialPosition?;
    private readonly particlesOptions;
    constructor(emitters: Emitters, container: Container, emitterOptions: IEmitter, position?: ICoordinates);
    play(): void;
    pause(): void;
    resize(): void;
    private prepareToDie;
    private destroy;
    private calcPosition;
    private emit;
}
