import type { IPlugin } from "../../Core/Interfaces/IPlugin";
import type { Container } from "../../Core/Container";
import { Absorbers } from "./Absorbers";
import type { RecursivePartial } from "../../Types";
import type { IAbsorberOptions } from "./Options/Interfaces/IAbsorberOptions";
import type { IOptions } from "../../Options/Interfaces/IOptions";
import { Options } from "../../Options/Classes/Options";
declare class AbsorbersPlugin implements IPlugin {
    readonly id: string;
    constructor();
    getPlugin(container: Container): Absorbers;
    needsPlugin(options?: RecursivePartial<IOptions & IAbsorberOptions>): boolean;
    loadOptions(options: Options, source?: RecursivePartial<IOptions & IAbsorberOptions>): void;
}
declare const plugin: AbsorbersPlugin;
export type { IAbsorberOptions };
export { plugin as AbsorbersPlugin };
export * from "./Enums";
