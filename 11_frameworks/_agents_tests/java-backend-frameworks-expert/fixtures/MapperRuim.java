package org.sample;

import org.mapstruct.*;

@Mapper(componentModel = "guice", injectionStrategy = InjectionStrategy.CONSTRUCTOR, unmappedTargetPolicy = ReportingPolicy.FATAL, foo = "bar")
public abstract class BadMapper {

    @Mapping(target = "a", source = "b", constant = "1")
    @Mapping(target = "t", expression = "new TimeAndFormat(s.getTime())")
    @Mapping(target = "u", expression = "java( UUID.randomUUID().toString() )")
    @Mapping(target = "v", source = "name")
    abstract Target map(Source s, Other o);

    abstract void upd(Source s, @MappingTarget Target t, @MappingTarget Target t2);

    @ValueMappings({
        @ValueMapping(source = MappingConstants.ANY_REMAINING, target = "A"),
        @ValueMapping(source = MappingConstants.ANY_UNMAPPED, target = "B"),
        @ValueMapping(source = MappingConstants.THROW_EXCEPTION, target = "C")
    })
    abstract String enumToString(OrderType t);
}

@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@interface Titles { }
