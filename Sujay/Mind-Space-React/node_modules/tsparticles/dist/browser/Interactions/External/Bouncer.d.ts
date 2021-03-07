import type { IExternalInteractor } from "../../Core/Interfaces/IExternalInteractor";
import type { Container } from "../../Core/Container";
export declare class Bouncer implements IExternalInteractor {
    private readonly container;
    constructor(container: Container);
    isEnabled(): boolean;
    interact(): void;
    reset(): void;
    private processMouseBounce;
    private singleSelectorBounce;
    private processBounce;
}
