import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
import type { Container } from "../../Core/Container";
import type { IDelta } from "../../Core/Interfaces/IDelta";
export declare class TrailMaker implements IExternalInteractor {
    private readonly container;
    private delay;
    constructor(container: Container);
    interact(delta: IDelta): void;
    isEnabled(): boolean;
    reset(): void;
}
