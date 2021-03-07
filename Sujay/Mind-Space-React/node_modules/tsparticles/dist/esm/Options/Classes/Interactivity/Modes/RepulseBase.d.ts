import type { IRepulseBase } from "../../../Interfaces/Interactivity/Modes/IRepulseBase";
import type { RecursivePartial } from "../../../../Types";
export declare abstract class RepulseBase implements IRepulseBase {
    distance: number;
    duration: number;
    speed: number;
    constructor();
    load(data?: RecursivePartial<IRepulseBase>): void;
}
