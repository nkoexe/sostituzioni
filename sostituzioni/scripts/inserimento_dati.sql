INSERT OR IGNORE INTO ora_predefinita VALUES
    ('1', '07:50', '08:40'),
    ('2', '08:40', '09:30'),
    ('3', '09:30', '10:20'),
    ('Prima Pausa', '10:20', '10:35'),
    ('4', '10:35', '11:25'),
    ('5', '11:25', '12:10'),
    ('Seconda Pausa', '12:10', '12:25'),
    ('6', '12:25', '13:15'),
    ('7', '13:15', '14:05');

INSERT OR IGNORE INTO visualizzazione VALUES
    ('online'),
    ('fisica');

INSERT OR IGNORE INTO classe VALUES
    ('1 Ea', 0),
    ('1 Eb', 0),
    ('1 La', 0),
    ('1 Lb', 0),
    ('1 C', 0),
    ('1 C/Lb', 0),
    ('1 S', 0),
    ('1 SAa', 0),
    ('1 SAb', 0),
    ('1 SUa', 0),
    ('1 SUb', 0),
    ('2 Ea', 0),
    ('2 Eb', 0),
    ('2 La', 0),
    ('2 Lb', 0),
    ('2 C', 0),
    ('2 C/Lb', 0),
    ('2 S', 0),
    ('2 SAa', 0),
    ('2 SAb', 0),
    ('2 SUa', 0),
    ('2 SUb', 0),
    ('3 Ea', 0),
    ('3 Eb', 0),
    ('3 La', 0),
    ('3 Lb', 0),
    ('3 La/Lb', 0),
    ('3 C', 0),
    ('3 S', 0),
    ('3 SAa', 0),
    ('3 SAb', 0),
    ('3 SUa', 0),
    ('3 SUb', 0),
    ('4 E', 0),
    ('4 La', 0),
    ('4 Lb', 0),
    ('4 C', 0),
    ('4 C/Lb', 0),
    ('4 S', 0),
    ('4 SA', 0),
    ('4 SUa', 0),
    ('4 SUb', 0),
    ('5 Ea', 0),
    ('5 Eb', 0),
    ('5 L', 0),
    ('5 C', 0),
    ('5 C/L', 0),
    ('5 S', 0),
    ('5 SA', 0),
    ('5 SUa', 0),
    ('5 SUb', 0),
    ('Eson. IRC', 0);

INSERT OR IGNORE INTO aula VALUES
    ('004', 0, 0),
    ('007', 0, 0),
    ('008', 0, 0),
    ('009', 0, 0),
    ('055', 0, 0),
    ('056', 0, 0),
    ('057', 0, 0),
    ('059', 0, 0),
    ('060', 0, 0),
    ('101', 1, 0),
    ('102', 1, 0),
    ('103', 1, 0),
    ('105', 1, 0),
    ('106', 1, 0),
    ('129', 1, 0),
    ('130', 1, 0),
    ('131', 1, 0),
    ('133', 1, 0),
    ('134', 1, 0),
    ('201', 2, 0),
    ('202', 2, 0),
    ('203', 2, 0),
    ('205', 2, 0),
    ('206', 2, 0),
    ('207', 2, 0),
    ('214', 2, 0),
    ('216', 2, 0),
    ('217', 2, 0),
    ('221', 2, 0),
    ('222', 2, 0),
    ('230', 2, 0),
    ('231', 2, 0),
    ('232', 2, 0),
    ('234', 2, 0),
    ('235', 2, 0),
    ('301', 3, 0),
    ('312', 3, 0),
    ('313', 3, 0),
    ('Prefabbricato C1', 0, 0),
    ('Prefabbricato C2', 0, 0),
    ('Palazzina', 0, 0),
    ('Kubo', 2, 0),
    ('Auditorium', 0, 0),
    ('Biblioteca', 0, 0),
    ('Laboratorio di chimica', 1, 0),
    ('Laboratorio di fisica', 1, 0),
    ('Laboratorio di biotecnologie', 1, 0),
    ('Laboratorio di scienze', 1, 0),
    ('Laboratorio di informatica - 013', -1, 0),
    ('Laboratorio di informatica - 012', -1, 0),
    ('Laboratorio di informatica - 302', 3, 0),
    ('Palestra', 0, 0),
    ('SCPAR', 0, 0),
    ('SCA', 0, 0),
    ('SPRE', 0, 0),
    ('SCE', 0, 0),
    ('SCPAL', 0, 0),
    ('SPAL', 0, 0),
    ('SA', 0, 0),
    ('SR', 0, 0),
    ('S1A', 1, 0),
    ('S1B', 1, 0),
    ('S1R', 1, 0),
    ('S2A', 2, 0),
    ('S2B', 2, 0),
    ('S2BC', 2, 0),
    ('S2R', 2, 0),
    ('S2V', 2, 0),
    ('S3', 3, 0);

INSERT OR IGNORE INTO aula_ospita_classe VALUES
    ('004', '5 SUa', 1),
    ('007', '5 SUb', 1),
    ('008', '1 Ea', 1),
    ('009', '4 SUb', 1),
    ('055', '2 SUa', 1),
    ('056', '1 SUb', 1),
    ('057', '1 SUa', 1),
    ('059', '2 SUb', 1),
    ('060', '5 SUa', 1),
    ('101', '3 SUb', 1),
    ('102', '5 Eb', 1),
    ('103', '2 Ea', 1),
    ('105', '3 Eb', 1),
    ('106', '3 Ea', 1),
    ('129', '2 SAa', 1),
    ('130', '2 Eb', 1),
    ('131', '3 SAb', 1),
    ('133', '3 SAa', 1),
    ('134', '1 Eb', 1),
    ('201', '1 C', 1),
    ('201', '1 Lb', 1),
    ('201', '1 C/Lb', 1),
    ('202', '3 C', 1),
    ('203', '1 SAb', 1),
    ('205', '2 C', 1),
    ('205', '2 Lb', 1),
    ('205', '2 C/Lb', 1),
    ('206', '5 C', 1),
    ('206', '5 L', 1),
    ('206', '5 C/L', 1),
    ('207', 'Eson. IRC', 1),
    ('214', '5 SA', 1),
    ('216', '4 C', 1),
    ('216', '4 Lb', 1),
    ('216', '4 C/Lb', 1),
    ('217', '4 SA', 1),
    ('221', '4 S', 1),
    ('222', '3 La', 1),
    ('222', '3 Lb', 1),
    ('222', '3 La/Lb', 1),
    ('230', '2 SAb', 1),
    ('231', '2 La', 1),
    ('232', '2 S', 1),
    ('234', '1 S', 1),
    ('235', '1 La', 1),
    ('301', '4 E', 1),
    ('312', '1 SAa', 1),
    ('313', '5 S', 1),
    ('Prefabbricato C1', '3 S', 1),
    ('Prefabbricato C2', '3 SUa', 1),
    ('Palazzina', '5 Ea', 1);
