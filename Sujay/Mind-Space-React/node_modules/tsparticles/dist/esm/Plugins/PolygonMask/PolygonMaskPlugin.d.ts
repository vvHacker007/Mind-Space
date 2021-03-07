import type { IPlugin } from "../../Core/Interfaces/IPlugin";
import { PolygonMaskInstance } from "./PolygonMaskInstance";
import type { Container } from "../../Core/Container";
import type { RecursivePartial } from "../../Types";
import type { IOptions } from "../../Options/Interfaces/IOptions";
import type { IPolygonMaskOptions } from "./Options/Interfaces/IPolygonMaskOptions";
import { Options } from "../../Options/Classes/Options";
declare class PolygonMaskPlugin implements IPlugin {
    readonly id: string;
    constructor();
    getPlugin(container: Container): PolygonMaskInstance;
    needsPlugin(options?: RecursivePartial<IOptions & IPolygonMaskOptions>): boolean;
    loadOptions(options: Options, source?: RecursivePartial<IOptions & IPolygonMaskOptions>): void;
}
declare const plugin: PolygonMaskPlugin;
export type { IPolygonMaskOptions };
export { plugin as PolygonMaskPlugin };
export * from "./Enums";
