from openfisca_aotearoa.entities import Person
from openfisca_core.model_api import *

"""
MSD Policy (retrieved August 2018 from )
    https://www.workandincome.govt.nz/map/card-services/community-services-card/qualifications.html

    To be able to receive a Community Services Card, a client must:

    *   receive an income tested benefit or
    *   be a child for whom an Orphans Benefit, an Unsupported Childs Benefit or a Child Disability Allowance is paid or
    *   receive a Residential Care Subsidy or
    *   receive New Zealand Superannuation and meet an income test or
    *   receive Veteran's Pension or
    *   receive weekly income compensation (paid by Veterans' Affairs) or
    *   receive weekly compensation (paid by Veterans' Affairs) or
    *   be a full time student, generally be ordinarily resident and meet an income test or

    *   for people with dependent children
        *   meet an income test and generally be ordinarily resident in New Zealand or
        *   be eligible to receive Working for Families Tax Credits (where Inland Revenue applies a Residency test)

    *   for people with no children:
        *   meet an income test
        *   generally be ordinarily resident and
        *   be aged over 16 years old, but not be a dependent child
"""


class social_security__eligible_for_community_services_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Eligible for Community Services Card"
    reference = "https://www.workandincome.govt.nz/map/card-services/community-services-card/qualifications.html"

    def formula(persons, period, parameters):
        # The applicant
        resident_or_citizen = persons('is_citizen_or_resident', period)
        age_requirement = persons("age", period) >= parameters(period).entitlements.social_security.community_services_card.age_threshold
        low_income = persons('community_services_card__below_income_threshold', period)
        dependent_children = persons('social_security__has_dependant_child', period)
        is_fulltime_student = persons('social_security__is_fulltime_student', period)
        received_superannuation = persons('social_security__received_supperannuation', period)
        eligible_for_wff = persons('income_tax__eligible_for_working_for_families', period.this_year)
        childs_benefit = \
            persons('social_security__received_orphans_benefit', period) +\
            persons('social_security__received_unsupported_childs_benefit', period) +\
            persons('social_security__received_child_disability_allowance', period)

        return \
            persons('social_security__received_income_tested_benefit', period.this_year) +\
            persons('social_security__received_residential_care_subsidy', period) +\
            persons('veterans_support__received_veterans_pension', period) +\
            persons('veterans_support__received_weekly_income_compensation', period) +\
            persons('veterans_support__received_weekly_compensation', period) +\
            childs_benefit +\
            (received_superannuation * low_income) +\
            (is_fulltime_student * low_income) +\
            (dependent_children * low_income * (resident_or_citizen + eligible_for_wff)) +\
            not_(dependent_children) * low_income * resident_or_citizen * age_requirement


# TODO:
# below are variables that still need to be implemented
class social_security__received_orphans_benefit(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class social_security__received_unsupported_childs_benefit(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class social_security__received_child_disability_allowance(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class social_security__received_residential_care_subsidy(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class veterans_support__received_veterans_pension(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class veterans_support__received_weekly_income_compensation(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"
    reference = "http://legislation.govt.nz/act/public/2014/0056/latest/link.aspx?id=DLM5537962"


class veterans_support__received_weekly_compensation(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"
    reference = "http://legislation.govt.nz/act/public/2014/0056/latest/link.aspx?id=DLM5602254"


class social_security__received_supperannuation(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"


class social_security__is_fulltime_student(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "TODO"
