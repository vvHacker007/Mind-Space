import type { IInfection } from "../../Interfaces/Infection/IInfection";
import type { RecursivePartial } from "../../../Types";
import { InfectionStage } from "./InfectionStage";
import type { IOptionLoader } from "../../Interfaces/IOptionLoader";
export declare class Infection implements IInfection, IOptionLoader<IInfection> {
    cure: boolean;
    delay: number;
    enable: boolean;
    infections: number;
    stages: InfectionStage[];
    constructor();
    load(data?: RecursivePartial<IInfection>): void;
}
