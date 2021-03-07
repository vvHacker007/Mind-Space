import type { Container } from "../../Core/Container";
import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
export declare class Grabber implements IExternalInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(): boolean;
    reset(): void;
    interact(): void;
}
