definition September() returns uint8 = 9;
definition October() returns uint8 = 10;
definition November() returns uint8 = 11;
definition December() returns uint8 = 12;

rule sistersBirthMonths(
    uint8 Sara,
    uint8 Ophelia,
    uint8 Nora,
    uint8 Dawn
) {
    // each sister was born in 1 of 4 months
    require Sara >= September() && Sara <= December();
    require Ophelia >= September() && Ophelia <= December();
    require Nora >= September() && Nora <= December();
    require Dawn >= September() && Dawn <= December();

    // each sister's initial is different from the initial of her birth month
    require(
        Sara != September() &&
        Ophelia != October() &&
        Nora != November() &&
        Dawn != December()
    );

    // Ophelia was not born in September
    require Ophelia != September();

    // Nora was not born in September
    require Nora != September();

    // Nora's month starts with a consonant
    require Nora != October();

    // sisters were born on different months
    require(
        Sara != Ophelia &&
        Sara != Nora &&
        Sara != Dawn &&
        Ophelia != Nora &&
        Ophelia != Dawn &&
        Nora != Dawn
    );

    satisfy true;
}

rule solutionIsUnique(
    uint8 Sara,
    uint8 Ophelia,
    uint8 Nora,
    uint8 Dawn
) {
    // each sister was born in 1 of 4 months
    require Sara >= September() && Sara <= December();
    require Ophelia >= September() && Ophelia <= December();
    require Nora >= September() && Nora <= December();
    require Dawn >= September() && Dawn <= December();

    // each sister's initial is different from the initial of her birth month
    require(
        Sara != September() &&
        Ophelia != October() &&
        Nora != November() &&
        Dawn != December()
    );

    // Ophelia was not born in September
    require Ophelia != September();

    // Nora was not born in September
    require Nora != September();

    // Nora's month starts with a consonant
    require Nora != October();

    // sisters were born on different months
    require(
        Sara != Ophelia &&
        Sara != Nora &&
        Sara != Dawn &&
        Ophelia != Nora &&
        Ophelia != Dawn &&
        Nora != Dawn
    );

    assert(
        Dawn == September() &&
        Sara == October() &&
        Ophelia == November() &&
        Nora == December()
    );
}
