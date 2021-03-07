import type { IContainerPlugin } from "../Core/Interfaces/IContainerPlugin";
import type { IPlugin } from "../Core/Interfaces/IPlugin";
import type { Container } from "../Core/Container";
import type { RecursivePartial } from "../Types";
import type { IOptions } from "../Options/Interfaces/IOptions";
import type { IShapeDrawer } from "../Core/Interfaces/IShapeDrawer";
import type { Options } from "../Options/Classes/Options";
export declare class Plugins {
    static getPlugin(plugin: string): IPlugin | undefined;
    static addPlugin(plugin: IPlugin): void;
    static getAvailablePlugins(container: Container): Map<string, IContainerPlugin>;
    static loadOptions(options: Options, sourceOptions: RecursivePartial<IOptions>): void;
    static getPreset(preset: string): RecursivePartial<IOptions> | undefined;
    static addPreset(presetKey: string, options: RecursivePartial<IOptions>): void;
    static addShapeDrawer(type: string, drawer: IShapeDrawer): void;
    static getShapeDrawer(type: string): IShapeDrawer | undefined;
    static getSupportedShapes(): IterableIterator<string>;
}
