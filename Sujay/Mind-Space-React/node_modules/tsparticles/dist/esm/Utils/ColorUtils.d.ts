import type { IColor, IRgb, IRgba, IHsl, IHsla, IHsv, IHsva } from "../Core/Interfaces/Colors";
import type { IImage } from "../Core/Interfaces/IImage";
import { IParticle } from "../Core/Interfaces/IParticle";
export declare class ColorUtils {
    static colorToRgb(input?: string | IColor, index?: number, useIndex?: boolean): IRgb | undefined;
    static colorToHsl(color: string | IColor | undefined, index?: number, useIndex?: boolean): IHsl | undefined;
    static rgbToHsl(color: IRgb): IHsl;
    static stringToAlpha(input: string): number | undefined;
    static stringToRgb(input: string): IRgb | undefined;
    static hslToRgb(hsl: IHsl): IRgb;
    static hslaToRgba(hsla: IHsla): IRgba;
    static hslToHsv(hsl: IHsl): IHsv;
    static hslaToHsva(hsla: IHsla): IHsva;
    static hsvToHsl(hsv: IHsv): IHsl;
    static hsvaToHsla(hsva: IHsva): IHsla;
    static hsvToRgb(hsv: IHsv): IRgb;
    static hsvaToRgba(hsva: IHsva): IRgba;
    static rgbToHsv(rgb: IRgb): IHsv;
    static rgbaToHsva(rgba: IRgba): IHsva;
    static getRandomRgbColor(min?: number): IRgb;
    static getStyleFromRgb(color: IRgb, opacity?: number): string;
    static getStyleFromHsl(color: IHsl, opacity?: number): string;
    static getStyleFromHsv(color: IHsv, opacity?: number): string;
    static mix(color1: IRgb | IHsl, color2: IRgb | IHsl, size1: number, size2: number): IRgb;
    static replaceColorSvg(image: IImage, color: IHsl, opacity: number): string;
    static getLinkColor(p1: IParticle, p2?: IParticle, linkColor?: string | IRgb): IRgb | undefined;
    static getLinkRandomColor(optColor: string | IColor, blink: boolean, consent: boolean): IRgb | string | undefined;
}
