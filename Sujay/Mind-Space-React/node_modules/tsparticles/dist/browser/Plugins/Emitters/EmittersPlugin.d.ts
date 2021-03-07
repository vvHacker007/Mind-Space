import type { IPlugin } from "../../Core/Interfaces/IPlugin";
import type { Container } from "../../Core/Container";
import { Emitters } from "./Emitters";
import type { RecursivePartial } from "../../Types";
import type { IOptions } from "../../Options/Interfaces/IOptions";
import type { IEmitterOptions } from "./Options/Interfaces/IEmitterOptions";
import { Options } from "../../Options/Classes/Options";
declare class EmittersPlugin implements IPlugin {
    readonly id: string;
    constructor();
    getPlugin(container: Container): Emitters;
    needsPlugin(options?: RecursivePartial<IOptions & IEmitterOptions>): boolean;
    loadOptions(options: Options, source?: RecursivePartial<IOptions & IEmitterOptions>): void;
}
declare const plugin: EmittersPlugin;
export type { IEmitterOptions };
export { plugin as EmittersPlugin };
export * from "./Enums";
