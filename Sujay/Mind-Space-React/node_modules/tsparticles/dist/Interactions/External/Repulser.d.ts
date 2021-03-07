import type { Container } from "../../Core/Container";
import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
export declare class Repulser implements IExternalInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(): boolean;
    reset(): void;
    interact(): void;
    private singleSelectorRepulse;
    private hoverRepulse;
    private processRepulse;
    private clickRepulse;
}
