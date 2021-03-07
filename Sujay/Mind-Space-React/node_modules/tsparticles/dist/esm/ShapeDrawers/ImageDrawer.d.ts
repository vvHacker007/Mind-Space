import type { IShapeDrawer } from "../Core/Interfaces/IShapeDrawer";
import type { IParticle } from "../Core/Interfaces/IParticle";
import type { IImage } from "../Core/Interfaces/IImage";
import type { Container } from "../Core/Container";
interface ContainerImage {
    id: string;
    images: IImage[];
}
export declare class ImageDrawer implements IShapeDrawer {
    images: ContainerImage[];
    constructor();
    getSidesCount(): number;
    getImages(container: Container): ContainerImage;
    addImage(container: Container, image: IImage): void;
    init(container: Container): Promise<void>;
    destroy(): void;
    private loadImageShape;
    draw(context: CanvasRenderingContext2D, particle: IParticle, radius: number, opacity: number): void;
}
export {};
