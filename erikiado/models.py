from django.db import models


class Prediction(models.Model):
    """ Main model of the family app.

    This models stores the main attributes and indicators
    of a family, it also serves as a HUB for the models
    that store the main data points from the socioeconomical
    studies.

    Attributes:
    -----------
    OPCIONES_ESTADO_CIVIL : tuple(tuple())
        This is a field that stores the list of options to be stored in the
        estado_civil field.
    OPCIONES_LOCALIDAD : tuple(tuple())
        This is a field that stores the list of options to be stored in the localidad field.
    numero_hijos_diferentes_papas : IntegerField
        The content of this field needs to be clarified with the stakeholder, whether this
        is the number of unique parents, the children of a mother have, or just the total
        number of children.
    explicacion_solvencia : TextField
        This field should be filled in their net mensual income is negative. It serves as an
        explanation on how the family deals with the deficit.
    estado_civil : TextField
        This field stores the information regarding the legal relationship status of the
        parents in a family.
    localidad : Text Field
        This field stores the town in which a family resides.

    TODO:
    -----

    - Implement total_neto field, total_egresos, and total_ingresos, once the ingresos and
    egresos tables are created.
    - Clarify the contents of the number_hijos_diferentes_papas field
    """

    img_url = models.TextField()
    # label = models.CharField()

    def __str__(self):
        """ Prints the texto attribute of this class.

        """
        return self.img_url
