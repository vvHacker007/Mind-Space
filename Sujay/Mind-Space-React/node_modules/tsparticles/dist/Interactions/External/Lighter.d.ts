import type { Container } from "../../Core/Container";
import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
export declare class Lighter implements IExternalInteractor {
    private readonly container;
    constructor(container: Container);
    interact(): void;
    isEnabled(): boolean;
    reset(): void;
}
