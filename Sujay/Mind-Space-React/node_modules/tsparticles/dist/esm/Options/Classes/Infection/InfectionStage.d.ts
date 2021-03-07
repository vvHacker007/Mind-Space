import type { IInfectionStage } from "../../Interfaces/Infection/IInfectionStage";
import { OptionsColor } from "../OptionsColor";
import type { RecursivePartial } from "../../../Types";
import type { IOptionLoader } from "../../Interfaces/IOptionLoader";
export declare class InfectionStage implements IInfectionStage, IOptionLoader<IInfectionStage> {
    color: OptionsColor;
    duration?: number;
    infectedStage?: number;
    radius: number;
    rate: number;
    constructor();
    load(data?: RecursivePartial<IInfectionStage>): void;
}
