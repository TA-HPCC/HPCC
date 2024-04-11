# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: p4/tmp/p4config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='p4/tmp/p4config.proto',
  package='p4.tmp',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x15p4/tmp/p4config.proto\x12\x06p4.tmp\"\xce\x01\n\x0eP4DeviceConfig\x12\x10\n\x08reassign\x18\x01 \x01(\x08\x12-\n\x06\x65xtras\x18\x02 \x01(\x0b\x32\x1d.p4.tmp.P4DeviceConfig.Extras\x12\x13\n\x0b\x64\x65vice_data\x18\x03 \x01(\x0c\x1a\x66\n\x06\x45xtras\x12\x31\n\x02kv\x18\x01 \x03(\x0b\x32%.p4.tmp.P4DeviceConfig.Extras.KvEntry\x1a)\n\x07KvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')
)




_P4DEVICECONFIG_EXTRAS_KVENTRY = _descriptor.Descriptor(
  name='KvEntry',
  full_name='p4.tmp.P4DeviceConfig.Extras.KvEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='p4.tmp.P4DeviceConfig.Extras.KvEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='p4.tmp.P4DeviceConfig.Extras.KvEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=199,
  serialized_end=240,
)

_P4DEVICECONFIG_EXTRAS = _descriptor.Descriptor(
  name='Extras',
  full_name='p4.tmp.P4DeviceConfig.Extras',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='kv', full_name='p4.tmp.P4DeviceConfig.Extras.kv', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_P4DEVICECONFIG_EXTRAS_KVENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=240,
)

_P4DEVICECONFIG = _descriptor.Descriptor(
  name='P4DeviceConfig',
  full_name='p4.tmp.P4DeviceConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reassign', full_name='p4.tmp.P4DeviceConfig.reassign', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extras', full_name='p4.tmp.P4DeviceConfig.extras', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_data', full_name='p4.tmp.P4DeviceConfig.device_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_P4DEVICECONFIG_EXTRAS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=240,
)

_P4DEVICECONFIG_EXTRAS_KVENTRY.containing_type = _P4DEVICECONFIG_EXTRAS
_P4DEVICECONFIG_EXTRAS.fields_by_name['kv'].message_type = _P4DEVICECONFIG_EXTRAS_KVENTRY
_P4DEVICECONFIG_EXTRAS.containing_type = _P4DEVICECONFIG
_P4DEVICECONFIG.fields_by_name['extras'].message_type = _P4DEVICECONFIG_EXTRAS
DESCRIPTOR.message_types_by_name['P4DeviceConfig'] = _P4DEVICECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

P4DeviceConfig = _reflection.GeneratedProtocolMessageType('P4DeviceConfig', (_message.Message,), dict(

  Extras = _reflection.GeneratedProtocolMessageType('Extras', (_message.Message,), dict(

    KvEntry = _reflection.GeneratedProtocolMessageType('KvEntry', (_message.Message,), dict(
      DESCRIPTOR = _P4DEVICECONFIG_EXTRAS_KVENTRY,
      __module__ = 'p4.tmp.p4config_pb2'
      # @@protoc_insertion_point(class_scope:p4.tmp.P4DeviceConfig.Extras.KvEntry)
      ))
    ,
    DESCRIPTOR = _P4DEVICECONFIG_EXTRAS,
    __module__ = 'p4.tmp.p4config_pb2'
    # @@protoc_insertion_point(class_scope:p4.tmp.P4DeviceConfig.Extras)
    ))
  ,
  DESCRIPTOR = _P4DEVICECONFIG,
  __module__ = 'p4.tmp.p4config_pb2'
  # @@protoc_insertion_point(class_scope:p4.tmp.P4DeviceConfig)
  ))
_sym_db.RegisterMessage(P4DeviceConfig)
_sym_db.RegisterMessage(P4DeviceConfig.Extras)
_sym_db.RegisterMessage(P4DeviceConfig.Extras.KvEntry)


_P4DEVICECONFIG_EXTRAS_KVENTRY._options = None
# @@protoc_insertion_point(module_scope)
