export class LineDrawer {
    getSidesCount() {
        return 1;
    }
    draw(context, particle, radius) {
        context.moveTo(0, -radius / 2);
        context.lineTo(0, radius / 2);
    }
}
