import enum
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Union
from uuid import UUID

from dataclasses_json import config
from dataclasses_json import dataclass_json
from marshmallow import fields
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import mapping
from shapely.geometry import shape


class GeometryField(fields.Field):
    """Вспомогательный класс, позволяющий преобразовывать `shapely`-объекты в `GeoJSON`-формат."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, list):
            return [mapping(item) for item in value]
        return mapping(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if isinstance(value, list):
            return [shape(item) for item in value]
        return shape(value)


class FunctionalAreaType(enum.IntEnum):
    """Функциональная зона сооружения.

    Attributes:
        :ONE: I.
        :TWO: II.
        :THREE: III.
        :FLARE_STACK_ZONE: Факельная зона.

    """
    ONE = 1
    TWO = 2
    THREE = 3
    FLARE_STACK_ZONE = 4


@dataclass_json
@dataclass
class Circle:
    """Круг.

    Attributes:
      :radius_m (float): значение радиуса круга в метрах.

    """
    radius_m: float = 0.


@dataclass_json
@dataclass
class Rectangle:
    """Прямоугольник.

    Шириной является вертикальная сторона, длиной -- горизонтальная.
          ______________
          |            |
    width |            |
          |____________|
              length

    Attributes:
        :width_m (float): значение ширины прямоугольника в метрах.
        :length_m (float): значение длины прямоугольника в метрах.

    """
    width_m: float = 0.
    length_m: float = 0.


@dataclass_json
@dataclass
class Position:
    """Координаты центра многоугольника здания.

    Attributes:
        :building_id (UUID): id сооружения.
        :offset_x_m (float): координаты по оси X, м.
        :offset_y_m (float): координаты по оси Y, м.
        :angle_deg (float): угол поворота здания вокруг его центра по часовой стрелке, градусы.

    """
    building_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    offset_x_m: float = 0.
    offset_y_m: float = 0.
    angle_deg: float = 0.


@dataclass_json
@dataclass
class ConnectionType:
    """Тип соединения.

    Обозначает тип соединения.
    Например:
     - трубопровод 114х6;
     - ВЛ 6кВ;

     Следует обратить внимание, что он служит только для конкретных сущностей(труба с определенным заданным диаметром),
     а не для абстракных(например, просто ВЛ без привязки к какому-либо напряжению или сечению провода).

     Attributes:
        :id (UUID): id типа соединения.
        :name (str): название типа соединения.
        :cost (float): удельная стоимость прокладки одного метра соединения.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    name: str = field(default_factory=str)
    cost: float = 0.


@dataclass_json
@dataclass
class ConnectionPoint:
    """Точка подключения строения.

    Координаты точки подключения вычисляются относительно центра фигуры.

    Attributes:
        :id (UUID): id точки подключения.
        :building_id (UUID): id сооружения.
        :point_m (Point): локальные координаты точки подключения для сооружения.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    building_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    point_m: Point = field(
        default_factory=Point,
        metadata=config(
            mm_field=GeometryField()
        ))


@dataclass_json
@dataclass
class Building:
    """Параметры здания/строения/сооружения.

    Attributes:
        :id (UUID): id параметров строения.
        :figure (Union[Circle, Rectangle]): геометрическая форма строения.
        :functional_area (FunctionalAreaType): функциональная зона сооружения.
        :connection_points (List[ConnectionPoint]): точки подключения.
        :label (str): обозначение на схеме.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    figure: Union[Circle, Rectangle] = field(default_factory=Circle)
    functional_area: FunctionalAreaType = FunctionalAreaType.ONE
    connection_points: List[ConnectionPoint] = field(default_factory=list)
    label: str = field(default_factory=str)


@dataclass_json
@dataclass
class BuildingOffsetRule:
    """Правило минимально-допустимого расстояния между строениями.

   Например: "Здание №1" должно находится на расстоянии от "Здание №2" не менее чем в 8 м.

   Attributes:
       :first_building_parameters_id (UUID): id параметров первого сооружения.
       :second_building_parameters_id (UUID): id параметров второго сооружения.
       :offset_m (float): минимальное допустимое расстояние между зданиями.

   """
    first_building_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    second_building_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    offset_m: float = 0.


@dataclass_json
@dataclass
class BuildingConnection:
    """Соединение между строениями.

    Например: "Здание №1" связано со "Здание №2" соединением типа "Трубопровод 114х6".

    Attributes:
        :id (UUID): id соединения.
        :source_connection_point_id (UUID): id точки подключения первого сооружения.
        :target_connection_point_id (UUID): id точки подключения второго сооружения.
        :connection_type_id (UUID): id типа соединения.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    source_connection_point_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    target_connection_point_id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    connection_type_id: UUID = UUID('00000000-0000-0000-0000-000000000000')


@dataclass_json
@dataclass
class BuildingCluster:
    """Группа сооружений.

     Attributes:
        :id (UUID): id группы сооружений.
        :building_ids (List[UUID]): список зданий, входящих в кластер.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    building_ids: List[UUID] = field(default_factory=list)


@dataclass_json
@dataclass
class BuildingClusterWithPositions:
    """Группа сооружений.

     Attributes:
        :id (UUID): id группы сооружений.
        :positions (List[UUID]): местоположение центров зданий, входящих в кластер.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    positions: List[Position] = field(default_factory=list)


@dataclass_json
@dataclass
class ExternalPoint:
    """Внешняя точка.

    Используется для оптимизации размещения сооружений. Сооружение, у которого есть внешняя точка подключения
    такого же типа, как и у данной внешней точки, должно размещаться ближе у границ генплана и как можно ближе к
    данной внешней точке.

    Attributes:
        :id (UUID): id внешней точки.
        :point (Point): координаты внешней точки на местности.
        :connection_point_type_id (UUID): тип точки подключения.

    """
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    point_m: Point = field(
        default_factory=Point,
        metadata=config(
            mm_field=GeometryField()
        ))
    connection_point_type_id: UUID = UUID('00000000-0000-0000-0000-000000000000')


@dataclass_json
@dataclass
class InputData:
    """Входные данные расчетной задачи.

   Attributes:
       :development_area_m (Polygon): допустимая область размещения генплана(область расчета).
       :connection_types (List[ConnectionType]): типы соединений.

       :buildings (List[BuildingParameters]): параметры сооружений, которые необходимо разместить.
       :building_offset_rules (List[BuildingOffsetRule]): минимальные допустимые расстояния между сооружениями.
       :building_connections (List[BuildingConnection]): соединения сооружений.
       :building_clusters (List[Union[BuildingCluster, BuildingClusterWithPositions]]): группы сооружений.

       :external_points (List[ExternalPoint]): внешние точки.
       :wind_rose_angle_deg (float): азимут преобладающего направления ветра (роза ветров).

   """
    development_area_m: Polygon = field(
        default_factory=Polygon,
        metadata=config(
            mm_field=GeometryField()
        ))
    connection_types: List[ConnectionType] = field(default_factory=list)
    buildings: List[Building] = field(default_factory=list)
    building_clusters: List[Union[BuildingCluster, BuildingClusterWithPositions]] = field(default_factory=list)
    building_offset_rules: List[BuildingOffsetRule] = field(default_factory=list)
    building_connections: List[BuildingConnection] = field(default_factory=list)

    external_points: List[ExternalPoint] = field(default_factory=list)
    wind_rose_angle_deg: float = 0.


@dataclass_json
@dataclass
class Solution:
    """Решение задачи поиска оптимальных местоположений зданий.

    Attributes:
        :positions (List[Position]): список местоположений зданий/строений/сооружений.

    """
    positions: List[Position] = field(default_factory=list)
