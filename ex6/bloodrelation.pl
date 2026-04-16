% --- Facts: Gender ---
male(moolam_thirunal_rama_varma).
male(uthradom_thirunal_marthanda_varma).
male(pooruruttathi_thirunal_marthanda_varma).
male(avittom_thirunal_aditya_varma).
male(anjaneya_varma).

female(aswathi_thirunal_gowri_lakshmi_bayi).
female(parvathidevi_kochamma).
female(gopika_nair).
female(anjali_bayi).

% --- Facts: Parents ---
% L1 to L2
parent(moolam_thirunal_rama_varma, uthradom_thirunal_marthanda_varma).
parent(moolam_thirunal_rama_varma, aswathi_thirunal_gowri_lakshmi_bayi).

% L2 to L3
parent(uthradom_thirunal_marthanda_varma, pooruruttathi_thirunal_marthanda_varma).
parent(uthradom_thirunal_marthanda_varma, avittom_thirunal_aditya_varma).
parent(aswathi_thirunal_gowri_lakshmi_bayi, parvathidevi_kochamma).

% L3 to L4
parent(pooruruttathi_thirunal_marthanda_varma, gopika_nair).
parent(avittom_thirunal_aditya_varma, anjali_bayi).
parent(parvathidevi_kochamma, anjaneya_varma).

% --- Relationship Rules ---

% 1. Child
child(Y, X) :- parent(X, Y).

% 2. Son
son(Y, X) :- male(Y), parent(X, Y).

% 3. Daughter
daughter(Y, X) :- female(Y), parent(X, Y).

% 4. Sibling (Common parent and X is not Y)
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.

% 5. Brother
brother(X, Y) :- male(X), sibling(X, Y).

% 6. Sister
sister(X, Y) :- female(X), sibling(X, Y).

% 7. Grandparent
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% 8. Ancestor (Recursive)
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
