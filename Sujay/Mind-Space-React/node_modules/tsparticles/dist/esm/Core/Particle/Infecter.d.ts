import type { Container } from "../Container";
export declare class Infecter {
    private readonly container;
    infectionStage?: number;
    infectionTime?: number;
    infectionDelay?: number;
    infectionDelayStage?: number;
    constructor(container: Container);
    startInfection(stage: number): void;
    updateInfectionStage(stage: number): void;
    updateInfection(delta: number): void;
    private nextInfectionStage;
}
