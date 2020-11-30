function calendar(element, objects, controller) {
    if(controller.calendar == null) { // lazy initialization
        controller.calendar = new FullCalendar.Calendar(element, {
            height: 'parent',
            editable: true,
            eventChange: function(info) {
                controller.changeDateProperty('date', controller.objects[info.event.extendedProps.index], info.event.start.getFullYear(),
                    info.event.start.getMonth() + 1,info.event.start.getUTCDate() + 1); // month and day are zero-based in full calendar
            },
            eventClick: function(info) {
                controller.changeSimpleGroupObject(controller.objects[info.event.extendedProps.index], false, info.el);
            }
        });
        setTimeout(function () {
            controller.calendar.render();
        }, 0);
    }

    controller.objects = objects; // need to save it to work with changes
    controller.calendar.setOption('events', objects.map((obj, index) =>
        Object.assign({}, obj, {
            index: index,
            classNames: controller.isCurrent(obj) ? 'event-highlight' : ''
        })));
}