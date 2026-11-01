package org.sample;

import org.mapstruct.*;
import org.mapstruct.factory.Mappers;

@Mapper(imports = UUID.class, componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface SourceTargetMapper {

    @Mapping(target = "id", source = "sourceId", defaultExpression = "java( UUID.randomUUID().toString() )")
    @Mapping(target = "stringConstant", constant = "Constant Value")
    @Mapping(target = "dateConstant", dateFormat = "dd-MM-yyyy", constant = "09-01-2014")
    Target sourceToTarget(Source s);

    @Mapping(target = "description", source = "person.description")
    @Mapping(target = "houseNumber", source = "address.houseNo")
    DeliveryAddressDto personAndAddressToDeliveryAddressDto(Person person, Address address);

    @ValueMappings({
        @ValueMapping(source = MappingConstants.NULL, target = "DEFAULT"),
        @ValueMapping(source = "STANDARD", target = MappingConstants.NULL),
        @ValueMapping(source = MappingConstants.ANY_REMAINING, target = "SPECIAL")
    })
    ExternalOrderType orderTypeToExternalOrderType(OrderType orderType);

    void updateCarFromDto(CarDto carDto, @MappingTarget Car car);
}
